# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'reportlab.lib.styles',
        'reportlab.platypus',
        'reportlab.lib.units',
        'openpyxl',
        'openpyxl.styles',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'PIL',
        'PIL.Image',
        'email',
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        'email.mime.application',
        'models',
        'models.database',
        'controllers',
        'controllers.app_controller',
        'views',
        'views.base_page',
        'views.login_page',
        'views.register_page',
        'views.user_dashboard_page',
        'views.dashboard_page',
        'views.slot_management_page',
        'views.vehicles_page',
        'views.payments_page',
        'views.profile_page',
        'views.settings_page',
        'views.reports_page',
        'views.admin_manage_page',
        'utils',
        'utils.config',
        'utils.helpers',
        'utils.pdf_generator',
        'utils.email_sender',
        'utils.excel_exporter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'unittest',
        'test',
        'tests',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,  # Faster startup - don't archive Python bytecode
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,  # Don't include binaries in EXE - use COLLECT instead
    name='SmartParkingSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX - faster startup
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Use COLLECT for one-folder distribution (much faster startup)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='SmartParkingSystem',
)
