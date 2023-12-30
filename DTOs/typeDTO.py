class typeDTO:
    def __init__(self, typeId, name):
        self.typeId = typeId
        self.name = name

    @classmethod
    def type(cls, typeId, name):
        obj = cls(typeId, name)
        return obj