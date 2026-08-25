import hashlib
import os
import tempfile

import requests

import config


CHUNK_SIZE = 1024 * 1024


def model_exists():
    path = config.LOCAL_MODEL_PATH
    return os.path.isfile(path) and os.path.getsize(path) > 100 * 1024 * 1024


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_model(progress_callback=None):
    """Download the NOVA local model once, then reuse it across app updates."""
    if model_exists():
        return config.LOCAL_MODEL_PATH

    os.makedirs(os.path.dirname(config.LOCAL_MODEL_PATH), exist_ok=True)
    fd, temp_path = tempfile.mkstemp(
        prefix="nova-model-", suffix=".part", dir=os.path.dirname(config.LOCAL_MODEL_PATH)
    )
    os.close(fd)

    try:
        with requests.get(config.LOCAL_MODEL_URL, stream=True, timeout=(20, 120)) as response:
            response.raise_for_status()
            total = int(response.headers.get("content-length", "0"))
            downloaded = 0

            with open(temp_path, "wb") as output:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if not chunk:
                        continue
                    output.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(downloaded, total)

        if config.LOCAL_MODEL_SHA256:
            actual = _sha256(temp_path)
            if actual.lower() != config.LOCAL_MODEL_SHA256.lower():
                raise RuntimeError(
                    "Downloaded NOVA model failed SHA-256 verification. "
                    "The file was not installed."
                )

        os.replace(temp_path, config.LOCAL_MODEL_PATH)
        return config.LOCAL_MODEL_PATH
    except Exception:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise
