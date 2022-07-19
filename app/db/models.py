from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CountryType


from database import Base


user_to_user = Table("user_to_use", Base.metadata,
    Column("left_user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("right_user_id", Integer, ForeignKey("user.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), default=False, unique=True)
    country = Column(CountryType)
    score = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    picture = Column(String(200))

    friends = relationship("user",
                        secondary=user_to_user,
                        primaryjoin=id==user_to_user.c.left_user_id,
                        secondaryjoin=id==user_to_user.c.right_user_id,
                        backref="left_user"
    )

