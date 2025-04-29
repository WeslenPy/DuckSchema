class MoneyManager:

    @staticmethod
    def formatter_brl(valor:float):
        valor =float(str(valor).replace(",","."))
        
        if isinstance(valor, (int, float)):
            valor_formatado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            return str(valor_formatado)
        else:
            return str(0)
        
