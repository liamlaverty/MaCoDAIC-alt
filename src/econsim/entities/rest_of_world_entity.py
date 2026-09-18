from src.econsim.entities.actor_entity import ActorEntity


class RestOfWorldEntity(ActorEntity):
    def __init__(self, id: int):
        super().__init__(name=f"RestOfWorldEntity_{id}")
        self.id = id