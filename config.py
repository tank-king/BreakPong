import os.path
import sys

screen_width = 800
screen_height = 900
FPS = 60

ASSETS = 'assets'

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
    ASSETS = os.path.join(sys._MEIPASS, ASSETS)
    import pyi_splash
    pyi_splash.close()
else:
    print('running in a normal Python process')
