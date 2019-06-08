# -*- mode: python -*-

block_cipher = None


a = Analysis(['ocean_analysis111.py'],
             pathex=['F:\\Documents\\sea'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [('SimHei.ttf','F:\\Documents\\sea\\SimHei.ttf','DATA')],
          name='ocean_analysis111',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='favicon.ico')
