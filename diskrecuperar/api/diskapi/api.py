
# from diskrecuperar.api.manager.response import Response
# from httpx import Response
# import httpx

# class DiskAPI:
    
#     def __init__(self) -> None:
        
    
#         self.api = 
    
    
#     def register(self,email:str,password:str) -> Response:
#         response: Response = httpx.post(,
#                               json=dict(email=email,password=password))
        
        
#         return Response(response=response)
    

import json
from PySide6.QtCore import (QUrl, QObject, Slot,Signal, 
                            QTimer,QByteArray,QUrlQuery)
from PySide6.QtNetwork import (QNetworkAccessManager, 
                               QNetworkRequest, 
                               QNetworkReply, 
                               QSslConfiguration)

class URLManager:
    
    URL_BASE = "http://127.0.0.1:8000/api/v1"
    
    
    @property
    def register(cls):
        return f"{cls.URL_BASE}/register/user"    
    
    @property
    def auth(cls):
        return f"{cls.URL_BASE}/auth/token"


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
        
        query = QUrlQuery()
        query.addQueryItem("password",data["password"])
        query.addQueryItem("username", data["username"])

        data:list = QByteArray()
        data.append(
            query.query(
                encoding=QUrl.ComponentFormattingOption.FullyEncoded
                    ).encode("utf-8"))

        self.reply = self.manager.post(request,data)

        self._start_timeout(self.reply,10000)
        
        
        
    def post(self, url: str,data:dict):
        request = QNetworkRequest(QUrl(url))

        # ssl_config: QSslConfiguration = QSslConfiguration.defaultConfiguration()
        # request.setSslConfiguration(ssl_config)

        request.setRawHeader(b"User-Agent", b"DiskAPI/1.0")
        request.setRawHeader(b"Accept", b"application/json")
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader,
                             "application/json")
        
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
        
        self.request_finished.emit(result)