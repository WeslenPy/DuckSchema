from duckschema import TOKEN

import json
from PySide6.QtCore import (QUrl, QObject, Slot,Signal, 
                            QTimer,QByteArray,QUrlQuery)
from PySide6.QtNetwork import (QNetworkAccessManager, 
                               QNetworkRequest, 
                               QNetworkReply, 
                               QSslConfiguration)
from urllib.parse import urlencode
class URLManager:
    
    URL_BASE = "http://159.203.132.92:80/api/v1"
    
    
    @property
    def register(cls):
        return f"{cls.URL_BASE}/register/user"    
    
    @property
    def auth(cls):
        return f"{cls.URL_BASE}/auth/token"
    
    
    @property
    def product_list(cls):
        return f"{cls.URL_BASE}/product/list"
    
    @property
    def purchased_new(cls):
        return f"{cls.URL_BASE}/purchased/new"
    
    
    @property
    def archive_download(cls):
        return f"{cls.URL_BASE}/archive/download"
    
    @property
    def archive_filter(cls):
        return f"{cls.URL_BASE}/archive/filter"


    @property
    def archive_like(cls):
        return f"{cls.URL_BASE}/archive/like"    
    
    @property
    def archive_favorite(cls):
        return f"{cls.URL_BASE}/archive/favorite"

    @property
    def archive_favorite_status(cls):
        return f"{cls.URL_BASE}/archive/favorite/status"

    @property
    def archive_like_status(cls):
        return f"{cls.URL_BASE}/archive/like/status"



class RequestManager(QObject):
    
    request_finished = Signal(dict) 
    def __init__(self):
        super().__init__()
        
        
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self._on_finished)

        self.reply_timers = {}
        
        self.url = URLManager()
        
    def form(self,url,data:dict):
        request = QNetworkRequest(QUrl(url))

        # ssl_config: QSslConfiguration = QSslConfiguration.defaultConfiguration()
        # request.setSslConfiguration(ssl_config)

        request.setRawHeader(b"User-Agent", b"DiskAPI/1.0")
        request.setRawHeader(b"Accept", b"application/json")
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, 
                             "application/x-www-form-urlencoded")
        
        if TOKEN.token:
            request.setRawHeader(b"Authorization", 
                            f"Bearer {TOKEN.token}".encode())
            
        

        query = QUrlQuery()
        for key,value in data.items():
            query.addQueryItem(key,value)
            
            
        data:list = QByteArray()
        data.append(
            query.query(
                encoding=QUrl.ComponentFormattingOption.FullyEncoded
                    ).encode("utf-8"))

        self.reply = self.manager.post(request,data)

        self._start_timeout(self.reply,10000)
        
        
    def query(self,url,data:dict={}):
        
        query_params =  urlencode(query=data)
        request = QNetworkRequest(QUrl(f"{url}?{query_params}"))

        # ssl_config: QSslConfiguration = QSslConfiguration.defaultConfiguration()
        # request.setSslConfiguration(ssl_config)

        request.setRawHeader(b"User-Agent", b"DiskAPI/1.0")
        request.setRawHeader(b"Accept", b"application/json")
        if TOKEN.token:
            request.setRawHeader(b"Authorization", 
                            f"Bearer {TOKEN.token}".encode())
            

        self.reply = self.manager.get(request)

        self._start_timeout(self.reply,10000)
        
        
    def get(self,url):
        
        request = QNetworkRequest(QUrl(url))

        # ssl_config: QSslConfiguration = QSslConfiguration.defaultConfiguration()
        # request.setSslConfiguration(ssl_config)

        request.setRawHeader(b"User-Agent", b"DiskAPI/1.0")
        request.setRawHeader(b"Accept", b"application/json")
        if TOKEN.token:
            request.setRawHeader(b"Authorization", 
                            f"Bearer {TOKEN.token}".encode())
            

        self.reply = self.manager.get(request)

        self._start_timeout(self.reply,10000)
        
        
        
    def post(self, url: str,data:dict):
        request = QNetworkRequest(QUrl(url))

        # ssl_config: QSslConfiguration = QSslConfiguration.defaultConfiguration()
        # request.setSslConfiguration(ssl_config)

        request.setRawHeader(b"User-Agent", b"DiskAPI/1.0")
        request.setRawHeader(b"Accept", b"application/json")
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader,
                             "application/json")
        
        if TOKEN.token:
            request.setRawHeader(b"Authorization", 
                            f"Bearer {TOKEN.token}".encode())
            
        
        data = QByteArray(json.dumps(data).encode(encoding='utf-8'))

        self.reply = self.manager.post(request,data)

        self._start_timeout(reply=self.reply,timeout=10000)

    def _start_timeout(self, reply: QNetworkReply, timeout: int):
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._on_timeout(reply))
        self.reply_timers[reply] = timer
        timer.start(timeout)

    def _on_timeout(self, reply: QNetworkReply):
        if reply.isRunning():
            reply.abort()
        self.reply_timers.pop(reply, None)
        result = {
            "success": False,
            "error": "Timeout da requisição"
        }
        self.request_finished.emit(result)


    @Slot()
    def _on_finished(self, reply: QNetworkReply):
        
        if len(self.reply_timers)>0:
            timer:QTimer= self.reply_timers.pop(reply, None)
            if timer:
                timer.stop()
                timer.deleteLater()


        if reply.error() != QNetworkReply.NetworkError.NoError:
            result = {
                "success": False,
                "error": reply.errorString()
            }
        else:
            raw_data = reply.readAll().data().decode()
            try:
                parsed = json.loads(raw_data)
                result = {"success": True, "data": parsed}
            except json.JSONDecodeError:
                result = {"success": True, "data": raw_data}
                
        reply.deleteLater()
        
        # print(result)
        self.request_finished.emit(result)