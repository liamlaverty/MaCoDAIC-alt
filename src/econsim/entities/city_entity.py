from src.econsim.entities.actor_entity import ActorEntity


class CityEntity(ActorEntity):
    def __init__(self):
        super().__init__(name="City")
        self.next_entity_id = 0