from setuptools import setup

APP = ['bash.py']
OPTIONS = {
    'argv_emulation': True,  # нужно для GUI-интеракций
    'packages': ['paramiko', 'scp'],
    'plist': {
        'CFBundleName': 'CSVUploader',
        'CFBundleDisplayName': 'CSVUploader',
        'CFBundleIdentifier': 'com.yourcompany.csvuploader',
        'CFBundleVersion': '0.1.0',
        'LSUIElement': True,  # скрыть иконку из дока (если нужно)
    }
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
