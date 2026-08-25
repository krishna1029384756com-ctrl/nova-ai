from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs

ROOT = Path(SPEC).resolve().parent.parent

datas = [
    (str(ROOT / "frontend"), "frontend"),
]

binaries = collect_dynamic_libs("llama_cpp")

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        "llama_cpp",
        "llama_cpp.llama",
        "llama_cpp.llama_chat_format",
    ],
    excludes=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="NOVA",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="NOVA",
)
