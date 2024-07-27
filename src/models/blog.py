from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from typing import Annotated
import datetime, os, sys
 
 
sys.path.append(os.path.join(sys.path[0][:-6]))

from database import Base

class Table_blog(Base):
    __tablename__ = "blog"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    date_published: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
