from duckschema.utils.manager.path import BasePath
from duckschema.utils.manager.extensions import Extensions
from pathlib import Path
from PySide6.QtGui import *
from PySide6.QtCore import *


class FontManager(BasePath,Extensions):
    
    def load_all_fonts(self):
        fonts = Path(self.font_path).glob("**/*.ttf")
        for font in fonts: QFontDatabase.addApplicationFont(font.as_posix())
            