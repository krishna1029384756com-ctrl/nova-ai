# NOVA Companion

NOVA Companion is the lightweight Android-side executor for NOVA AI.

## Purpose

The companion is **not an AI** and is **not a file-transfer application**. Its purpose is to provide an on-demand, authenticated communication bridge between NOVA on the PC and an Android device, and later execute permitted UI tasks on the phone.

### Design rules

- No LLM or intelligence in the APK.
- No file transfer functionality.
- No always-on background service.
- Communication is activated only when the user starts a NOVA phone-control session.
- The PC remains responsible for understanding and planning natural-language requests.
- The Android side receives structured operations and returns structured results.
- Android security boundaries must not be bypassed.

## First milestone

The first implementation target is deliberately small:

1. Start the companion manually.
2. Discover/connect to the NOVA PC on the local network.
3. Establish a paired session.
4. Send `PING`.
5. Receive `PONG`.
6. Disconnect cleanly.

Phone UI automation will be added only after the communication layer is reliable.
