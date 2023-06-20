from pydantic import BaseModel


class Card(BaseModel):
    title: str
    type: str
    is_gooj: bool = False

    class Config:
        orm_mode = True

    def __repr__(self) -> str:
        return f"title: {self.title}, type: {self.type}"
