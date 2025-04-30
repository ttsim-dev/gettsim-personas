from gettsim_personas.load_personas import load_personas

gettsim_personas = load_personas()

# Expose each persona as an attribute
for persona in gettsim_personas.personas:
    setattr(gettsim_personas, persona.name, persona)
