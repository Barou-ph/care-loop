from __future__ import annotations
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

Severity = Literal["P0", "P1", "P2"]
Status = Literal["NEW", "ACKNOWLEDGED", "RESOLVED", "FALSE_ALARM"]

class EventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    household_id: Optional[str] = Field(default=None, max_length=100)
    device_id: Optional[str] = Field(default=None, max_length=100)
    event_type: str = Field(min_length=2, max_length=80)
    severity: Severity = "P1"
    source: str = Field(default="fall_detection", max_length=80)
    track_id: Optional[int] = Field(default=None, ge=0)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
    occurred_at: Optional[str] = Field(default=None, max_length=40)
    metadata: dict[str, Any] = Field(default_factory=dict)
    actor: str = Field(default="system", max_length=100)

class EventAction(BaseModel):
    actor: str = Field(min_length=1, max_length=100)
    note: Optional[str] = Field(default=None, max_length=1000)

class DeviceCreate(BaseModel):
    device_id: str = Field(min_length=1, max_length=100)
    household_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=120)
    device_type: str = Field(default="camera", max_length=50)
