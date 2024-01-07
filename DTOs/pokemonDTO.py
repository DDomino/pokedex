class pokemonDTO:
    
    def __init__(self, id, name, species, height, weight, abilityone, abilitytwo, abilitythree,typeone, typetwo, entry, gen, image, prev, next):
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
        self.prev = prev
        self.next = next

    @classmethod
    def create_object(cls, id, name, species, height, weight, abilityone, abilitytwo, abilitythree, typeone, typetwo, entry, gen, image, prev, next):
        obj =  cls(id, name, species, height, weight, abilityone, abilitytwo, abilitythree, typeone, typetwo, entry, gen, image, prev, next )
        return obj