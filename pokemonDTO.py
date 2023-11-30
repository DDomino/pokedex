class pokemonDTO:
    
    def __init__(self, id, name, species, height, weight, abilityone, abilitytwo, abilitythree,typeone, typetwo, entry, gen, genus, image, prev, next):
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
        self.genus = genus
        self.image = image
        self.prev = prev
        self.next = next

    @classmethod
    def create_object(cls, id, name, species, height, weight, abilityone, abilitytwo, abilitythree, typeone, typetwo):
        obj =  cls(id, name.capitalize(), species, height, weight, abilityone, abilitytwo, abilitythree, typeone, typetwo, None, None, None, None, None, None )
        return obj