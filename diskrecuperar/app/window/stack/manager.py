from diskrecuperar.app.window.pages.home.widget import HomePage
from diskrecuperar.app.window.pages.search.widget import SearchPage
from diskrecuperar.app.window.pages.history.widget import HistoryPage
from diskrecuperar.app.window.pages.security.widget import LoginPage
from diskrecuperar.app.window.pages.security.register import RegisterPage
from PySide6.QtWidgets import QStackedWidget


class PageManager:
    def __init__(self,stack:QStackedWidget) -> None:
        
        self.home_page = HomePage(stack)
        self.search_page = SearchPage(stack)
        self.history_page = HistoryPage(stack)
        self.download_page = HistoryPage(stack)
        self.login_page = LoginPage(stack)
        self.register_page = RegisterPage(stack)
        