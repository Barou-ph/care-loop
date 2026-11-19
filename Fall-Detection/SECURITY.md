# Security Notes

CARE LOOP V3 is a local prototype, not a production service.

## Safe local use

- The supplied Windows launcher binds the API to `127.0.0.1`, not a public interface.
- The API key is optional for local development. If configured, set `CARE_LOOP_API_KEY` in both the API and desktop processes.
- Keep the API on loopback. Do not port-forward it or expose it to a LAN/public network.
- Use a long random API key if testing beyond a single local process.
- Do not commit `.env` files, database files, camera recordings, or private video datasets.
- The desktop application can save annotated videos. Disable that option if video retention is not wanted.

## Current limitations

- The shared API key is not user authentication and does not provide caregiver roles or per-household authorization.
- SQLite is configured for a single local service instance.
- Event delivery is best-effort and has no durable retry/outbox.
- No production encryption-at-rest, retention policy, consent workflow, or emergency notification provider is implemented.
- AI alerts are unverified suspicions and must be checked by a human caregiver.

## Reporting

For a private project deployment, report security issues to the repository maintainer through the project's designated private contact channel. Do not include credentials, private camera footage, or personal data in public issue reports.
