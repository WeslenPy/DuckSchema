from diskrecuperar.utils.manager.path import BasePath
from diskrecuperar.utils.manager.extensions import Extensions
from pathlib import Path
from PySide6.QtGui import *
from PySide6.QtCore import *


class CssManager(BasePath,Extensions):
        
    def read_file(self,path:str):
        css_style_file = QFile(path)
        css_style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        
        stream = QTextStream(css_style_file)
        data_file = stream.readAll()
        css_style_file.close()
        
        return data_file
        
    def get_dark(self):
        dark_path = self.joinpath("dark.css",self.css_theme_path)
        css_style_file =self.read_file(dark_path.as_posix())
        return css_style_file
    
    def get_light(self):
        light_path = self.joinpath("light.css",self.css_theme_path)
        css_style_file =self.read_file(light_path.as_posix())
        return css_style_file
            
    
    def load_all_css(self,app:QCoreApplication):
        qcss_files = Path(self.css_path).glob("styles/*.*")
        
        final_css = self.get_dark()
        for css_path in qcss_files:
            css_style_file =self.read_file(css_path.as_posix())
            final_css += css_style_file
        
            
        app.setStyleSheet(final_css)
                    