from sqlalchemy.orm import Mapped, mapped_column

import sys
import os 

sys.path.append(os.path.join(sys.path[0][:-6]))

from database import Base

class Table_Admins(Base):
    __tablename__ = "admins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(default="0")
    login: Mapped[str]
    password: Mapped[str]