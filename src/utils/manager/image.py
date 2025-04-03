from src.utils.manager.path import BasePath
from src.utils.manager.extensions import Extensions
from pathlib import Path
from PyQt6 import QtGui

class ImageManager(BasePath,Extensions):
    
    def get_filename(self,filename:str,type_file:str,path:Path)->Path:
        return self.joinpath(filename+str(type_file),path) 
    
    
    def get_ico(self,filename:str)->QtGui.QIcon:
        path= self.get_filename(filename,self.type_svg,self.svg_icon_path) 
        
        pixmap = QtGui.QPixmap(path.as_posix()).scaled(24, 24) 
        return QtGui.QIcon(pixmap)
                   
    def get_ico_by_png(self,filename:str)->QtGui.QIcon:
        path= self.get_filename(filename,self.type_png,self.png_icon_path) 
        return QtGui.QIcon(path.as_posix())
               
    def get_png(self,filename:str)-> QtGui.QPixmap:
        path =  self.get_filename(filename,self.type_png,self.png_icon_path)        
        return QtGui.QPixmap(path.as_posix())
    
    def get_svg(self,filename:str)-> QtGui.QPixmap:
        path =  self.get_filename(filename,self.type_svg,self.svg_icon_path)        
        return QtGui.QPixmap(path.as_posix())    
    
    
    def get_menu_svg_icon(self,filename:str)-> QtGui.QPixmap:
        path =  self.get_filename(filename,self.type_svg,self.svg_menu_path)        
        return QtGui.QIcon(path.as_posix())
        
    def get_svg_logo(self,filename:str)-> QtGui.QPixmap:
        path =  self.get_filename(filename,self.type_svg,self.svg_logo_path)        
        return path.as_posix()
    
    def get_png_logo(self,filename:str)-> QtGui.QPixmap:
        path =  self.get_filename(filename,self.type_png,self.png_logo_path)        
        return path.as_posix()
    
    
                      
    # def get_jpg(self,filename:str)-> QtGui.QPixmap:
    #     path =  self.get_filename(filename,self.type_jpg,self.png_path)        
    #     return QtGui.QPixmap(path.as_posix())
    
    def get_background(self)-> QtGui.QImage:
        path =  self.get_filename("img",self.type_jpg,self.background_img_path)        
        return QtGui.QImage(path.as_posix())
        