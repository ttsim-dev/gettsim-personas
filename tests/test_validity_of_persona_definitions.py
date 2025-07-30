"""Test that all persona definitions are valid."""

from gettsim_personas.orig_personas import orig_personas


def is_weakly_consecutive_increasing(id_values) -> bool:
    """Check if a list of integers is weakly consecutive increasing starting from 0."""
    if id_values[0] != 0:
        return False
    last = 0
    for val in id_values:
        if val < last or val > last + 1:
            return False
        last = val
    return True


def test_p_ids_are_consecutive():
    """Test that all p_ids in persona files are weakly consecutive increasing."""
    all_personas = orig_personas()

    for path, persona_collection in all_personas.items():
        for persona in persona_collection.personas:
            p_id_array = persona.input_data_tree.get("p_id")
            if not is_weakly_consecutive_increasing(p_id_array):
                msg = (
                    f"'p_id's in at least one persona at '{path}' are not weakly "
                    f"consecutive increasing: {p_id_array}"
                )
                raise ValueError(msg)
