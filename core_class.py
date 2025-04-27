from pydantic import BaseModel

class TradeInput(BaseModel):
    symbol: str        # e.g., "AAPL.NS" or "RELIANCE.NS"
    average_price: float
    quantity: int 
