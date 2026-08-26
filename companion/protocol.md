# NOVA Companion Protocol

## V0.1 Scope

The protocol is intentionally small. It carries commands and results only and does not transfer files.

### Message Envelope

Every message has a task/session identifier and a message type.

```json
{
  "id": "T0001",
  "type": "ping"
}