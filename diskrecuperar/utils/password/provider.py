import bcrypt


class PasswordProvider:
    
    @staticmethod
    def verify(password:str,password_input:str)->str:
        return bcrypt.checkpw(str.encode(password),str.encode(password_input))
    
    
    @staticmethod
    def crypto(password:str)->str:
        return bcrypt.hashpw(str.encode(password),bcrypt.gensalt(25,prefix=str.encode("H2X21S")))
    
    
    