
from httpx import Response


class Response:
    def __init__(self,response:Response) -> None:
        self.response = response
        
        
        
    @property
    def json(cls)->dict:
        return cls.response.json
        
        
    @property
    def status_code(cls)->int:
        return cls.response.status_code
    
    @property
    def message(cls):
        return cls.json.get("message",
                            "Erro ao estabelecer comunicação com servidor!")
    
    