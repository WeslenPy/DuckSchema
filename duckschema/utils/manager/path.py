from pathlib import Path,PurePath
import sys,os


class BasePath:
    
    ROOT_PATH:Path  = PurePath(Path.cwd())
    
    BASE_STATIC:str = "duckschema/static/"
    
    STATIC_PATH:Path = Path.joinpath(ROOT_PATH,BASE_STATIC)
    
    FONT_PATH =  Path.joinpath(STATIC_PATH,"font")
    
    CSS_PATH:Path = Path.joinpath(STATIC_PATH,"css")
    CSS_THEME_PATH:Path = Path.joinpath(CSS_PATH,"theme")
    
    BACKGROUND_PATH:Path = Path.joinpath(STATIC_PATH,"img/png/background")
    
    SVG_PATH:Path = Path.joinpath(STATIC_PATH,"img/svg")
    PNG_PATH:Path = Path.joinpath(STATIC_PATH,"img/png")
    
    SVG_ICON_PATH:Path = Path.joinpath(SVG_PATH,"icon")
    SVG_LOGO_PATH:Path = Path.joinpath(SVG_PATH,"logo")
    SVG_MENU_PATH:Path = Path.joinpath(SVG_PATH,"menu")
    
    PNG_LOGO_PATH:Path = Path.joinpath(PNG_PATH,"logo")
    PNG_ICON_PATH:Path = Path.joinpath(PNG_PATH,"icon")
    
    
    
    @property
    def root_path(cls)->Path:
        return cls.ROOT_PATH 
    
    @property
    def font_path(cls)->Path:
        return cls.FONT_PATH
      
    @property
    def css_path(cls)->Path:
        return cls.CSS_PATH 
    
    @property
    def css_theme_path(cls)->Path:
        return cls.CSS_THEME_PATH
    
    @property
    def static_path(cls)->Path:
        return cls.STATIC_PATH    
    
    
    @property
    def background_img_path(cls)->Path:
        return cls.BACKGROUND_PATH   
    
    @property
    def svg_icon_path(cls)->Path:
        return cls.SVG_ICON_PATH    
    
    @property
    def svg_logo_path(cls)->Path:
        return cls.SVG_LOGO_PATH   
    
    @property
    def png_logo_path(cls)->Path:
        return cls.PNG_LOGO_PATH   

    @property
    def svg_menu_path(cls)->Path:
        return cls.SVG_MENU_PATH   
    
    @property
    def png_icon_path(cls)->Path:
        return cls.PNG_ICON_PATH
    
    def joinpath(self,joined:str,root_path:Path):
        return Path.joinpath(root_path,joined)
    
    @classmethod
    def get_download_dir(cls):
        if sys.platform.startswith("win"):
            return Path(os.path.join(os.environ["USERPROFILE"],
                                     "Downloads")).as_posix()
        elif sys.platform.startswith("darwin"):
            return Path.home() / "Downloads"
        else:  
            return Path.home() / "Downloads"