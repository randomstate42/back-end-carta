from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    Country: str
    picture: str

    class config:
        orm_mode = True


class UserCreate(UserBase):
    something: int


class User(UserBase):
    score: int
    is_active: bool
    games_played: int
    games_won: int
    games_lost: int

    class Config:
        orm_mode = True


class UserLeaderboard(UserBase):
    score: int

class UserPosition(UserBase):
    rank: int

