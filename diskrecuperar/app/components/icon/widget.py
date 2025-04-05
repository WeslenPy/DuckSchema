from diskrecuperar.utils.manager.image import ImageManager
from PyQt6.QtGui import QIcon

class Icon(ImageManager):
    
    @property
    def add_plus(cls)->QIcon:
        return cls.get_ico("add_plus")  
        
    @property
    def bank(cls)->QIcon:
        return cls.get_ico("bank")  
        
    @property
    def confirm(cls)->QIcon:
        return cls.get_ico("confirm")  
    
    
    @property
    def gallery(cls)->QIcon:
        return cls.get_ico("gallery")  
    
        
    @property
    def trash(cls)->QIcon:
        return cls.get_ico("trash")  
    
    @property
    def cancel(cls)->QIcon:
        return cls.get_ico("cancel")
            
    @property
    def search(cls)->QIcon:
        return cls.get_ico("search")
        
    @property
    def edit(cls)->QIcon:
        return cls.get_ico("edit")
    
    @property
    def arrow_down(cls)->QIcon:
        
        return cls.get_ico("arrow_down")    
    
    @property
    def arrow_up(cls)->QIcon:
        
        return cls.get_ico("arrow_up")