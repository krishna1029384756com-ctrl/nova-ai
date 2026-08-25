# NOVA Companion Protocol

The companion uses a small JSON message envelope and does not transfer files.

```json
{"id":"T0001","type":"ping"}
```

Future task example:

```json
{"id":"T0002","type":"task","op":"YT_SEARCH","query":"what is HTML"}
```

The Android executor returns structured results such as `TASK_COMPLETED`, `TARGET_NOT_FOUND`, `ACTION_NOT_AVAILABLE`, `PERMISSION_REQUIRED`, `TIMEOUT`, and `TASK_FAILED`.

Pairing and authentication belong to the connection layer. Android security must not be bypassed, and credentials must not be placed in model prompts or ordinary task messages.
