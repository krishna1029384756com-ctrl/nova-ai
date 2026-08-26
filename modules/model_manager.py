import hashlib
import os
import shutil
import sys
import tempfile

import requests

import config


CHUNK_SIZE = 1024 * 1024


def _bundled_model_path():
    """Return the model shipped with the NOVA installer, when present."""
    roots = [getattr(sys, "_MEIPASS", None), os.path.dirname(sys.executable)]
    for root in roots:
        if root:
            candidate = os.path.join(root, "models", config.LOCAL_MODEL_FILENAME)
            if os.path.isfile(candidate):
                return candidate
    return None


def model_exists():
    path = config.LOCAL_MODEL_PATH
    return os.path.isfile(path) and os.path.getsize(path) > 100 * 1024 * 1024


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify(path):
    if config.LOCAL_MODEL_SHA256:
        actual = _sha256(path)
        if actual.lower() != config.LOCAL_MODEL_SHA256.lower():
            raise RuntimeError("NOVA model failed SHA-256 verification.")


def _install_bundled_model(source):
    os.makedirs(os.path.dirname(config.LOCAL_MODEL_PATH), exist_ok=True)
    temp_path = config.LOCAL_MODEL_PATH + ".part"
    try:
        shutil.copyfile(source, temp_path)
        _verify(temp_path)
        os.replace(temp_path, config.LOCAL_MODEL_PATH)
        return config.LOCAL_MODEL_PATH
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def ensure_model(progress_callback=None):
    """Ensure the NOVA local model exists in writable AppData.

    Priority:
    1. Existing AppData model.
    2. Model bundled inside the MSI/portable build.
    3. Verified download from Hugging Face.
    """
    if model_exists():
        return config.LOCAL_MODEL_PATH

    bundled = _bundled_model_path()
    if bundled:
        return _install_bundled_model(bundled)

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

        _verify(temp_path)
        os.replace(temp_path, config.LOCAL_MODEL_PATH)
        return config.LOCAL_MODEL_PATH
    except Exception:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise
