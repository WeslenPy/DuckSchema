from src.utils.manager.image import ImageManager

class Icon(ImageManager):
    
    @property
    def add_plus(cls):
        return cls.get_ico("add_plus")  
        
    @property
    def bank(cls):
        return cls.get_ico("bank")  
        
    @property
    def confirm(cls):
        return cls.get_ico("confirm")  
    
    
    @property
    def gallery(cls):
        return cls.get_ico("gallery")  
    
        
    @property
    def trash(cls):
        return cls.get_ico("trash")  
    
    @property
    def cancel(cls):
        return cls.get_ico("cancel")
            
    @property
    def search(cls):
        return cls.get_ico("search")
        
    @property
    def edit(cls):
        return cls.get_ico("edit")
    
    @property
    def arrow_down(cls):
        
        return cls.get_ico("arrow_down")    
    
    @property
    def arrow_up(cls):
        
        return cls.get_ico("arrow_up")