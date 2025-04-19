from PySide6.QtCore import *
import requests
from pathlib import Path
import tempfile,shutil

import time
from collections import deque

MAX_CONCURRENT_DOWNLOADS = 1
semaphore = QSemaphore(MAX_CONCURRENT_DOWNLOADS)

class DownloadSignals(QObject):
    progress = Signal(int)
    finished = Signal(bool)
    cancel = Signal(bool)
    velocity = Signal(float)
    status = Signal(bool)
    file = Signal(str)
    error = Signal(bool)


class DownloadTask(QRunnable):
    def __init__(self, url,folder:str):
        super().__init__()
        
        self.url:str = url
        self.folder:str = folder
        self.signals = DownloadSignals()
        
        self.cancelled = False
        
    def setCancel(self):
        self.cancelled = True

    def run(self):
        
        if self.cancelled:
            return
        
        self.signals.status.emit(False)
        semaphore.acquire()  # Aguarda se limite for atingido
        
        if self.cancelled:
            semaphore.release()
            return
        
        
        try:
            filename = self.url.split("/")[-1]
            filepath = Path(self.folder).joinpath(filename).as_posix()
            temp_dir = Path(tempfile.mkdtemp())
            temp_path= Path(temp_dir).joinpath(filename).as_posix()
            
            self.signals.file.emit(filepath)
        
            with requests.get(self.url, stream=True, timeout=60) as r:
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
            
        except RuntimeError:
            pass
            
        except Exception as e:
            self.signals.error.emit(True)
            
        finally:
            semaphore.release()  # Libera uma vaga no pool