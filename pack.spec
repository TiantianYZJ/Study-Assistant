# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['TaskWing.py'], 
    pathex=[],  
    binaries=[], 
    datas=[
        ('LOGO.png', '.'), 
        ('LOGO.ico', '.'), 
        ('azure.tcl', '.'), 
        ('theme/light.tcl', 'theme'), 
        ('theme/dark.tcl', 'theme'), 
        ('theme/light/*', 'theme/light'), 
        ('theme/dark/*', 'theme/dark'), 
        ('templates/ai_response.html', 'templates'), 
        ('templates/tutorial.html', 'templates'), 
        ('sound/*', 'sound'), 
    ],
    hiddenimports=[], 
    hookspath=[], 
    hooksconfig={},
    runtime_hooks=[], 
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='学翼', 
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, 
    icon='LOGO.ico',
    uac_admin=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='学翼V1.0.9' 
)