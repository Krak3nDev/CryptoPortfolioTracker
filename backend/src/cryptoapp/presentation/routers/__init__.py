from fastapi import Depends
from fastapi.security import HTTPBearer

security = Depends(HTTPBearer())
