from pydantic import BaseModel


class QuoteCurrency(BaseModel):
    price: float


class Quote(BaseModel):
    USD: QuoteCurrency


class Cryptocurrency(BaseModel):
    id: int
    name: str
    symbol: str
    slug: str
    is_active: int
    is_fiat: int
    quote: Quote
