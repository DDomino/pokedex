CREATE TABLE dexentries(
    id SERIAL PRIMARY key,
    pokemonid INTEGER,
    generation VARCHAR(20),
    dexentry TEXT,
    language varchar(20),
    unique (pokemonid, generation, language)
);


CREATE TABLE pokemon(
id SERIAL PRIMARY KEY,
pokedexid INTEGER UNIQUE NOT NULL,
pokemonname VARCHAR(100) UNIQUE NOT NULL,
pokemonspecies VARCHAR (100) NOT NULL,
pokemonheight NUMERIC(5,1) NOT NULL,
pokemonweight NUMERIC(5,1) NOT NULL,
pokemonabilityone INTEGER,
pokemonabilitytwo INTEGER,
pokemonabilitythree INTEGER,
typeone INTEGER,
typetwo INTEGER
);

CREATE INDEX idx_pokemonname ON pokemon(pokemonname);

CREATE TABLE abilities(
    id SERIAL PRIMARY KEY,
    abilityid INTEGER UNIQUE NOT NULL,
    abilityname VARCHAR(20) UNIQUE NOT NULL,
    abilityeffect TEXT
);

CREATE INDEX idx_abilityid ON abilities(abilityid)

CREATE TABLE types(
    id SERIAL PRIMARY KEY,
    typeid INTEGER UNIQUE NOT NULL,
    type VARCHAR(10) NOT NULL
);

CREATE INDEX idx_typeid ON types(typeid)


CREATE TABLE generations(
    id SERIAL PRIMARY KEY,
    generationid INTEGER UNIQUE NOT NULL,
    generationname text NOT NULL
);

CREATE INDEX idx_generationid ON generations(generationid);
