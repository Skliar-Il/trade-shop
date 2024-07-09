from fastapi import APIRouter
from fastapi import Depends

import os, sys 

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import get_async_session


router = APIRouter(
    prefix="/shop",
    tags="Shop"
)

