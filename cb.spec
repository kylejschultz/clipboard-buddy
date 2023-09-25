# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['clipboard-buddy.py'],
    pathex=[],
    binaries=[],
    datas=[('src/', 'src/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Clipboard Buddy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Clipboard Buddy',
)
app = BUNDLE(
    coll,
    name='Clipboard Buddy.app',
    icon='src/icon.icns',
    bundle_identifier='com.kjschultz.clipboard-buddy',
    info_plist={
        'LSUIElement': 'Yes',
    },
)
