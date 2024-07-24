from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from typing import Annotated
import datetime
import os 
import sys
 
 
sys.path.append(os.path.join(sys.path[0][:-6]))

from database import Base

class Table_products(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    full_description: Mapped[str]
    short_description: Mapped[str]
    date_published: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    price: Mapped[float | None]
    contacts: Mapped[str]
    # id: Mapped[int] = mapped_column(primary_key = True)
    # tg_id: Mapped[int]
    # tg_teg: Mapped[str]
    # subscribe: Mapped[bool] = mapped_column(default=False, nullable=False)
    # create_time: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    

    