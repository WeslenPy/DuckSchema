#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets,QtCore,QtGui
from duckschema.app.window.layout.home.window import Home
from duckschema.database.config.base import Model
from duckschema.database.config.conn import engine
from duckschema.database.model import *
from duckschema.utils.manager.path import BasePath
from duckschema.utils.manager.font import FontManager
from duckschema.utils.manager.css import CssManager
import sys



if __name__ == "__main__":
    

    app = QtWidgets.QApplication(sys.argv)
    screen_rect =  app.primaryScreen().availableGeometry()
    w, h = screen_rect.width(), screen_rect.height()
    centralWindow = screen_rect.center()
    
    
    FontManager().load_all_fonts()
    CssManager().load_all_css(app=app)
    
    window = Home()
    window.show()
    window.setFocus()
    Model.metadata.create_all(engine)
    
    font = QtGui.QFont("Roboto",8)
    app.setFont(font)
    

    sys.exit(app.exec())
