#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets,QtCore,QtGui
from duckschema.app.window.layout.home.window import Home
from duckschema.app.window.layout.security.window import Login
from duckschema.database.config.base import Model
from duckschema.database.config.conn import engine
from duckschema.database.model import *
from duckschema.utils.manager.path import BasePath
from duckschema.utils.manager.font import FontManager
from duckschema.utils.manager.css import CssManager
import sys,os,tempfile



if __name__ == "__main__":
    
    #SPLASH SCREEN NUITKA
    
    if "NUITKA_ONEFILE_PARENT" in os.environ:
        splash_filename = os.path.join(
            tempfile.gettempdir(),
            f"onefile_{ int(os.environ['NUITKA_ONEFILE_PARENT'])}_splash_feedback.tmp",
        )

        if os.path.exists(splash_filename):
            os.unlink(splash_filename)



    app = QtWidgets.QApplication(sys.argv)
    screen_rect =  app.primaryScreen().availableGeometry()
    w, h = screen_rect.width(), screen_rect.height()
    centralWindow = screen_rect.center()
    
    
    FontManager().load_all_fonts()
    CssManager().load_all_css(app=app)
    
    window = Login()
    window.show()
    window.setFocus()
    Model.metadata.create_all(engine)
    
    font = QtGui.QFont("Roboto",8)
    app.setFont(font)
    

    sys.exit(app.exec())
