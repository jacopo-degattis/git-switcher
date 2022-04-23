from setuptools import setup

APP = ['src/main.py']
DATA_FILES = ["src/config.json"]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'src/git-logo.png',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name='Gitswitch',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)