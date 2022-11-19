from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\wuwan\\Documents\\JOMO\\'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('Code/main.kv','C:\\Users\\wuwan\\Documents\\JOMO\\main.kv','DATA')]
a.datas += [('Code/data.py','C:\\Users\\wuwan\\Documents\\JOMO\\data.py','DATA')]
a.datas += [('Code/snippet.py','C:\\Users\\wuwan\\Documents\\JOMO\\snippet.py','DATA')]
a.datas += [('Code/sql_service.py','C:\\Users\\wuwan\\Documents\\JOMO\\sql_service.py','DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe, Tree('C:\\Users\\wuwan\\Documents\\JOMO\\snippets-master\\'),
               a.binaries,
               a.zipfiles,
               a.datas, 
	       *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],	
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')