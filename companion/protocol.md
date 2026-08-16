# NOVA Companion Protocol

## V0.1 scope

The protocol is intentionally tiny. It carries commands and results only. It does not transfer files.

### Message envelope

Every message has a task/session identifier and a message type.

```json
{
  "id": "T0001",
  "type": "ping"
}
```

## Initial messages

### PING

PC -> phone:

```json
{
  "id": "T0001",
  "type": "ping"
}
```

### PONG

Phone -> PC:

```json
{
  "id": "T0001",
  "type": "result",
  "status": "success",
  "code": "PONG"
}
```

## Future task shape

The AI will eventually convert natural language into structured operations. The phone must never receive the user's original natural-language request as the control protocol.

Example:

```json
{
  "id": "T0002",
  "type": "task",
  "op": "YT_SEARCH",
  "query": "what is HTML"
}
```

The phone executor returns a compact result, for example:

```json
{
  "id": "T0002",
  "type": "result",
  "status": "success",
  "code": "TASK_COMPLETED"
}
```

Possible result codes include `TASK_COMPLETED`, `TARGET_NOT_FOUND`, `APP_NOT_FOUND`, `ACTION_NOT_AVAILABLE`, `AUTH_REQUIRED`, `PERMISSION_REQUIRED`, `TIMEOUT`, and `TASK_FAILED`.

## Security boundary

Pairing and authentication belong to the connection layer. Android's own security mechanisms must not be bypassed. Credentials must not be placed into model prompts, model memory, or ordinary task messages.
