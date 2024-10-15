# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct
from dotenv import load_dotenv

# Load environment variables from .env file (if needed for other metadata)
load_dotenv()

COMPANY_NAME = os.getenv("COMPANY_NAME", "Default Company")
PRODUCT_NAME = os.getenv("PRODUCT_NAME", "JiggleWiggle")
FILE_DESCRIPTION = os.getenv("FILE_DESCRIPTION", "JiggleWiggle Mouse Jiggler App")
COPYRIGHT = os.getenv("COPYRIGHT", "Copyright © 2024 Your Company Name")
ORIGINAL_FILENAME = os.getenv("ORIGINAL_FILENAME", "jglwgl.exe")

# Read the version dynamically from version.txt
version_file_path = os.path.join(os.path.abspath("."), "version.txt")
try:
    with open(version_file_path, 'r') as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "1.0.0"  # Fallback to default if version.txt is not found

# Set up the version resource info using VSVersionInfo
version_resource = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=tuple(map(int, VERSION.split('.'))) + (0,),  # File version in tuple form (major, minor, revision, build)
        prodvers=tuple(map(int, VERSION.split('.'))) + (0,),  # Product version
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',  # Language and codepage (US English, Unicode)
                    [
                        StringStruct('CompanyName', COMPANY_NAME),
                        StringStruct('FileDescription', FILE_DESCRIPTION),
                        StringStruct('FileVersion', VERSION),
                        StringStruct('InternalName', PRODUCT_NAME),
                        StringStruct('LegalCopyright', COPYRIGHT),
                        StringStruct('OriginalFilename', ORIGINAL_FILENAME),
                        StringStruct('ProductName', PRODUCT_NAME),
                        StringStruct('ProductVersion', VERSION),
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [0x0409, 0x04B0])])
    ]
)

# PyInstaller spec setup
block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('version.txt', '.'),  # Ensure version.txt is bundled
        ('assets/icon.ico', 'assets')  # Bundle the icon in the assets folder
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='jglwgl',  # Name the executable 'jglwgl.exe'
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a console window to appear
    icon='assets/icon.ico',  # App icon
    version=version_resource  # Use dynamically created version info from version.txt
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JiggleWiggle'
)
