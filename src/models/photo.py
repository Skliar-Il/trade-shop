from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, ForeignKey
from typing import Annotated
import datetime
import os 
import sys
 
 
sys.path.append(os.path.join(sys.path[0][:-6]))

from database import Base


class Table_photos(Base):
    __tablename__ = "photos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    photo_link: Mapped[str]