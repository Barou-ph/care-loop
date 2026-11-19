import sys
import types

import numpy as np

# The state-machine tests do not instantiate YOLO. Keep the test independent of
# the optional ultralytics runtime while importing the active pipeline module.
try:
    import ultralytics  # noqa: F401
except ImportError:
    sys.modules["ultralytics"] = types.SimpleNamespace(YOLO=object)

from fall_detection_all_in_one import FallStateMachine, Tracklet


def make_track(in_zone=False):
    kps = np.zeros((17, 3), dtype=np.float32)
    track = Tracklet(1, [100, 100, 160, 200], kps, timestamp=0.0)
    track.in_occlusion_zone = in_zone
    track.occlusion_zone_name = "Table" if in_zone else None
    track.fsm = {
        "top0": 100.0,
        "top0_clipped": False,
        "hip0": 180.0,
        "upper0": 120.0,
        "h0": 100.0,
        "event_t": 0.0,
        "clock": 0.0,
        "down_time": 0.0,
        "hidden_time": 0.0,
        "peak_omega": 0.0,
        "recover_time": 0.0,
    }
    return track


def features(**overrides):
    data = {
        "top_y": 145.0,
        "truncated_top": False,
        "upper_y": 145.0,
        "hip_y": 215.0,
        "angle_valid": True,
        "torso_angle": 20.0,
        "head_up": False,
        "torso_ratio": 0.15,
        "aspect_ratio": 1.4,
        "bbox_height": 55.0,
        "truncated": False,
    }
    data.update(overrides)
    return data


def test_forward_fall_has_multiple_down_posture_signals():
    track = make_track()
    assert FallStateMachine()._is_down(track, features()) is True


def test_bending_with_hips_remaining_high_is_not_a_fall():
    track = make_track()
    assert FallStateMachine()._is_down(
        track,
        features(top_y=125.0, hip_y=182.0, torso_angle=25.0, aspect_ratio=0.8, bbox_height=90.0),
    ) is False


def test_sitting_upright_is_not_a_fall_even_if_body_box_gets_shorter():
    track = make_track()
    assert FallStateMachine()._is_down(
        track,
        features(
            top_y=135.0, hip_y=205.0, torso_angle=82.0, head_up=True,
            torso_ratio=0.30, aspect_ratio=0.8, bbox_height=60.0,
        ),
    ) is False


def test_side_fall_can_be_detected_when_torso_angle_is_unclear():
    track = make_track()
    assert FallStateMachine()._is_down(
        track,
        features(
            top_y=160.0, hip_y=225.0, angle_valid=False,
            aspect_ratio=1.5, bbox_height=45.0,
        ),
    ) is True


def test_occluded_upright_pose_is_not_enough_to_confirm_fall():
    track = make_track(in_zone=True)
    assert FallStateMachine()._is_down(
        track,
        features(
            top_y=150.0, hip_y=185.0, torso_angle=82.0, head_up=True,
            torso_ratio=0.30, aspect_ratio=0.8, bbox_height=80.0,
        ),
    ) is False


def test_occluded_horizontal_pose_can_supply_down_evidence():
    track = make_track(in_zone=True)
    assert FallStateMachine()._is_down(
        track,
        features(top_y=150.0, hip_y=215.0, torso_angle=20.0, aspect_ratio=1.2),
    ) is True


def test_disappearing_in_furniture_zone_without_down_evidence_does_not_alarm():
    track = make_track(in_zone=True)
    track.state = FallStateMachine.STATE_RAPID_DESCENT
    track.seen_down = False
    machine = FallStateMachine(occluded_confirm_sec=0.7)
    state, _ = machine.step_missing(track, 0.4)
    state, _ = machine.step_missing(track, 0.8)
    assert state == FallStateMachine.STATE_RAPID_DESCENT


def test_disappearing_after_observed_down_pose_can_confirm_fall():
    track = make_track(in_zone=True)
    track.state = FallStateMachine.STATE_RAPID_DESCENT
    track.seen_down = True
    machine = FallStateMachine(occluded_confirm_sec=0.7)
    machine.step_missing(track, 0.4)
    state, _ = machine.step_missing(track, 0.8)
    assert state == FallStateMachine.STATE_FALL_DETECTED
