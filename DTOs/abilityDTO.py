class abilityDTO:
    def __init__(self, id, name, effect):
        self.id = id
        self.name = name
        self.effect = effect
    
    @classmethod
    def ability(cls, id, name, effect):
        obj = cls(id, name, effect)
        return obj