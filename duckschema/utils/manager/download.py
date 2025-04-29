from PySide6.QtCore import *
import requests
from pathlib import Path
import tempfile,shutil

import time
from collections import deque
from urllib.parse import ParseResult, urlparse


MAX_CONCURRENT_DOWNLOADS = 1
semaphore = QSemaphore(MAX_CONCURRENT_DOWNLOADS)
tasking = False


class DownloadSignals(QObject):
    ondownload = Signal(int)
    progress = Signal(int)
    finished = Signal(bool)
    cancel = Signal(bool)
    velocity = Signal(float)
    status = Signal(bool)
    file = Signal(str)
    error = Signal(bool)


class DownloadTask(QRunnable):
    def __init__(self, filename):
        super().__init__()
        
        self.signals = DownloadSignals()
        self.filename = filename
        
        self.cancelled = False
        
        
    def setURL(self,url:str):
        self.url =url
          
    def setFolder(self,folder:str):
        self.folder =folder
        
    def setCancel(self):
        self.cancelled = True

    def run(self):
        
        if self.cancelled:
            return
    
        available = semaphore.available()
        self.signals.ondownload.emit(available)
        
        if not available:
            return self.signals.cancel.emit(True)
            
        
        self.signals.status.emit(False)
        semaphore.acquire()  
        
        if self.cancelled:
            semaphore.release()
            return
        
        try:
            
            url_parse: ParseResult = urlparse(url=self.url)
            querystring: str= url_parse.query
            uri = url_parse.scheme + "://" + url_parse.netloc + url_parse.path  
            
            
            filepath = Path(self.folder).joinpath(self.filename).as_posix()
            
            temp_dir = Path(tempfile.mkdtemp())
            temp_path= Path(temp_dir).joinpath(self.filename).as_posix()
            
            self.signals.file.emit(filepath)
            
            headers = {"User-Agent": "insomnia/2023.5.8"}
            
            
            with requests.request(method="GET", url=uri, 
                                  data="",  headers=headers, 
                                  params=querystring,stream=True,
                                  timeout=60) as r:
                
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                downloaded = 0

                self.signals.status.emit(True)
                
                speed_window = deque(maxlen=5)  # Últimos 5 segundos
                time_window = deque(maxlen=5)
                last_time = time.time()

                with  open(temp_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if self.cancelled:
                            self.signals.cancel.emit(True)
                            break
                        if chunk:
                            now = time.time()
                            elapsed = now - last_time
                            last_time = now
                            
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int((downloaded / total) * 100)
                            self.signals.progress.emit(percent)

                            if elapsed > 0:
                                speed_window.append(len(chunk))
                                time_window.append(elapsed)

                                total_speed = sum(speed_window) / sum(time_window)  # bytes/sec
                                speed_mbps = total_speed / (1024 * 1024)

                                self.signals.velocity.emit(float(f"{speed_mbps:.2f}"))
                                

            if not self.cancelled:
                shutil.move(str(temp_path), filepath)
                self.signals.finished.emit(True)
            
        except RuntimeError as erro:
            self.signals.cancel.emit(True)
            self.signals.error.emit(True)
            
        except Exception as erro:
            self.signals.cancel.emit(True)
            self.signals.error.emit(True)
            
        finally:
            semaphore.release()  # Libera uma vaga no pool