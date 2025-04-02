from src.app.window.pages.home.widget import HomePage
from src.app.window.pages.search.widget import SearchPage
from src.app.window.pages.history.widget import HistoryPage
from PyQt6.QtWidgets import QStackedWidget


class PageManager:
    def __init__(self,stack:QStackedWidget) -> None:
        
        self.home_page = HomePage(stack)
        self.search_page = SearchPage(stack)
        self.history_page = HistoryPage(stack)
        