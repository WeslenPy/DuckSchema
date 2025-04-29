from duckschema.app.window.pages.home.widget import HomePage
from duckschema.app.window.pages.search.widget import SearchPage
from duckschema.app.window.pages.history.widget import HistoryPage
from duckschema.app.window.pages.security.widget import LoginPage
from duckschema.app.window.pages.security.register import RegisterPage
from duckschema.app.window.pages.store.widget import StorePage
from PySide6.QtWidgets import QStackedWidget


class PageManager:
    def __init__(self,stack:QStackedWidget) -> None:
        
        self.home_page = HomePage(stack,pages=self)
        self.search_page = SearchPage(stack,pages=self)
        # self.history_page = HistoryPage(stack,pages=self)
        # self.download_page = HistoryPage(stack,pages=self)
        self.store_page = StorePage(stack,pages=self)
        
        
class PageLogin:
    def __init__(self,stack:QStackedWidget) -> None:
        
        self.login_page = LoginPage(stack,pages=self)
        self.register_page = RegisterPage(stack,pages=self)
        
        