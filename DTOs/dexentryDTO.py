class dexentryDTO:
    def __init__(self, pokemonId, generation, entry, language):
        self.pokemonId = pokemonId
        self.generation = generation
        self.entry = entry
        self.language = language

    @classmethod
    def create_object(cls, pokemonId, generation, entry, language):
        obj = cls(pokemonId, generation, entry, language)
        return obj