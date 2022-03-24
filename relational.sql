CREATE TABLE public.pokemon
(
    pokemon_id numeric,
    identifier text,
    species_id numeric,
    height numeric,
    weight numeric,
    base_experience numeric,

    PRIMARY KEY(pokemon_id)

);


CREATE TABLE public.abilities
(
    ability_id numeric,
    identifier text,


    PRIMARY KEY(ability_id)

);

CREATE TABLE public.types
(
    type_id numeric,
    identifier text,
    PRIMARY KEY (type_id)

);


CREATE TABLE public.regions
(
    region_id numeric,
    identifier text,

    PRIMARY KEY (region_id)

);


CREATE TABLE public.pokemon_types
(
    pokemon_id numeric,
    type_id numeric,

    Primary KEY(type_id, pokemon_id),
    FOREIGN KEY(type_id) REFERENCES types(type_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id)

);


CREATE TABLE public.pokemon_abilities
(
    pokemon_id numeric,
    ability_id numeric,

    Primary KEY(ability_id, pokemon_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY(ability_id) REFERENCES abilities(ability_id)

);




CREATE TABLE public.locations
(
    location_id numeric,
    region_id numeric,
    identifier text,


    Primary KEY(location_id),
    FOREIGN KEY(region_id) REFERENCES regions(region_id)

);


CREATE TABLE public.location_areas
(
    location_area_id numeric,
    location_id numeric,



    Primary KEY(location_area_id),
    FOREIGN KEY(location_id) REFERENCES locations(location_id)

);


CREATE TABLE public.encounters
(
    encounter_id numeric,
    location_area_id numeric,
    pokemon_id numeric,



    Primary KEY(encounter_id),
    FOREIGN KEY(location_area_id) REFERENCES location_areas(location_area_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id)

);