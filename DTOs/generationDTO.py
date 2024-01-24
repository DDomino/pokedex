class generationDTO:
    def __init__(self, id, name):
        self.id = id,
        self.name = name
    
    @classmethod
    def create_object(cls, id, name):
        obj = cls(id, name)
        return obj
    