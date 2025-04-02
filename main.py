

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets,QtCore,QtGui
from src.app.window.layout.home.window import Home
from src.database.config.base import Model
from src.database.config.conn import engine
from src.database.model import *
from src.utils.manager.path import BasePath
from src.utils.manager.font import FontManager
from src.utils.manager.css import CssManager
import sys



if __name__ == "__main__":
    

    app = QtWidgets.QApplication(sys.argv)
    screen_rect =  app.primaryScreen().availableGeometry()
    w, h = screen_rect.width(), screen_rect.height()
    centralWindow = screen_rect.center()
    
    
    FontManager().load_all_fonts()
    CssManager().load_all_css(app=app)
    
    window = Home()
    window.showMaximized()
    window.setFocus()
    Model.metadata.create_all(engine)
    
    font = QtGui.QFont("Roboto",8)
    app.setFont(font)
    

    sys.exit(app.exec())
