from pydantic import BaseModel, ConfigDict


class Card(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    type: str
    is_gooj: bool = False

    def __repr__(self) -> str:
        return f"title: {self.title}, type: {self.type}"
