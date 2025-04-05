from diskrecuperar.utils.manager.path import BasePath
from diskrecuperar.utils.manager.extensions import Extensions
from pathlib import Path
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class FontManager(BasePath,Extensions):
    
    def load_all_fonts(self):
        fonts = Path(self.font_path).glob("**/*.ttf")
        for font in fonts: QFontDatabase.addApplicationFont(font.as_posix())
            