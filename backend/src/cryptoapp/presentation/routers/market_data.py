from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

market_router = APIRouter(prefix="/market_data", route_class=DishkaRoute)

#
# @market_router.get("/currencies")
# async def fetch_currencies(interactor: FromDishka[CoinMarketApi]):
#     return {"message": "Fetching current currency data"}
