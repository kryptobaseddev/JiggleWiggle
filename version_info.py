import os
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

COMPANY_NAME = os.getenv("COMPANY_NAME", "Default Company")
PRODUCT_NAME = os.getenv("PRODUCT_NAME", "Default Product")
FILE_DESCRIPTION = os.getenv("FILE_DESCRIPTION", "Default Description")
VERSION = os.getenv("VERSION", "1.0.0")
COPYRIGHT = os.getenv("COPYRIGHT", "Default Copyright")
ORIGINAL_FILENAME = os.getenv("ORIGINAL_FILENAME", "app.exe")

VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=tuple(map(int, VERSION.split('.')) + [0]),  # File version
        prodvers=tuple(map(int, VERSION.split('.')) + [0]),  # Product version
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
