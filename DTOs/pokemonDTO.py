class pokemonDTO:
    
    def __init__(self, id, name, species, height, weight, abilityone, abilitytwo, abilitythree,typeone, typetwo, entry, gen, image):
        self.id = id
        self.name = name
        self.species = species
        self.height = height
        self.weight = weight
        self.abilityone = abilityone
        self.abilitytwo = abilitytwo
        self.abilitythree = abilitythree
        self.typeone = typeone
        self.typetwo = typetwo
        self.entry = entry
        self.gen = gen
        self.image = image


    @classmethod
    def create_object(cls, id, name, species, height, weight, abilityone, abilitytwo, abilitythree, typeone, typetwo, entry, gen, image):
        obj =  cls(id, name, species, height, weight, abilityone, abilitytwo, abilitythree, typeone, typetwo, entry, gen, image)
        return obj