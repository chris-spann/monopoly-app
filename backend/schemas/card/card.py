from pydantic import BaseModel, ConfigDict

from .card_actions import actions


class Card(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    type: str
    is_gooj: bool = False
    action_code: str

    def action(self, player_id: int):
        return actions[self.action_code](self.action_code, player_id)

    def __repr__(self) -> str:
        return f"title: {self.title}, type: {self.type}"
