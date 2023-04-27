# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_entry_point, copy_metadata
import lamancha

# Collect all available pytest plugins.
datas, hidden = collect_entry_point("pytest11")
for distribution in lamancha.collect_dependencies("lamancha[test]"):
    datas += copy_metadata(distribution)

a = Analysis(['frozen-pytest.py'],
             pathex=[SPECPATH],
             binaries=[],
             datas=datas,
             hiddenimports=hidden + ["lamancha.pyqt5"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='frozen-pytest',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='frozen-pytest')
