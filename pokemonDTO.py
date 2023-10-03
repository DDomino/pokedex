import re

class pokemonDTO:
    def __init__(self, id, name, entry, gen, genus, image, prev, next):
        self.name = name
        self.id = id
        self.entry = entry
        self.gen = gen
        self.genus = genus
        self.image = image
        self.prev = prev
        self.next = next

def create_object(id, name, entry, gen, genus, image, prev, next):
    obj = pokemonDTO(id, name.capitalize(), entry, gen.capitalize(), genus.capitalize(), image, prev, next)
    return obj