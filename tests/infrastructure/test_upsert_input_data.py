import dags.tree as dt
import numpy as np
import pytest

from _gettsim_personas.upsert import (
    broadcast_foreign_keys,
    broadcast_group_ids,
    broadcast_p_id,
    upsert_input_data,
)


@pytest.mark.parametrize(
    (
        "p_id_array",
        "expected_length",
        "expected_p_id",
    ),
    [
        (np.array([0, 1, 2]), 3, [0, 1, 2]),
        (np.array([0, 1, 2]), 6, [0, 1, 2, 3, 4, 5]),
    ],
)
def test_broadcast_p_id(p_id_array, expected_length, expected_p_id):
    broadcasted_p_id = broadcast_p_id(p_id_array, expected_length)
    assert np.array_equal(broadcasted_p_id, np.array(expected_p_id))


def test_broadcasting_p_id_fails_if_p_id_is_not_consecutive():
    p_id_array = np.array([0, 2, 3])
    expected_length = 3
    with pytest.raises(ValueError, match="Persona p_id does not start with 0 or"):
        broadcast_p_id(p_id_array, expected_length)


def test_broadcasting_p_id_fails_if_p_id_is_not_starting_with_0():
    p_id_array = np.array([1, 2, 3])
    expected_length = 3
    with pytest.raises(ValueError, match="Persona p_id does not start with 0 or"):
        broadcast_p_id(p_id_array, expected_length)


@pytest.mark.parametrize(
    (
        "original_array",
        "expected_length",
        "expected_array",
    ),
    [
        (np.array([0, 1, 2]), 3, np.array([0, 1, 2])),
        (np.array([0, 1, 2]), 6, np.array([0, 1, 2, 3, 4, 5])),
        (np.array([0, 0, 0]), 6, np.array([0, 0, 0, 1, 1, 1])),
        (np.array([0, 3, 5]), 6, np.array([0, 3, 5, 6, 9, 11])),
    ],
)
def test_broadcast_array_with_group_or_foreign_keys(
    original_array, expected_length, expected_array
):
    broadcasted_array = broadcast_group_ids(original_array, expected_length)
    assert np.array_equal(broadcasted_array, expected_array)


@pytest.mark.parametrize(
    (
        "original_array",
        "expected_length",
        "expected_array",
    ),
    [
        (np.array([0, 1, 2]), 6, np.array([0, 1, 2, 3, 4, 5])),
        (np.array([-1, 0, 2]), 6, np.array([-1, 0, 2, -1, 3, 5])),
    ],
)
def test_broadcast_foreign_keys(original_array, expected_length, expected_array):
    broadcasted_array = broadcast_foreign_keys(original_array, expected_length)
    assert np.array_equal(broadcasted_array, expected_array)


@pytest.mark.parametrize(
    (
        "data_from_persona",
        "data_to_upsert",
        "expected_upserted_data",
    ),
    [
        # p_id and simple array updated
        (
            {
                "p_id": np.array([0, 1, 2]),
                "a": np.array([0, 1, 2]),
            },
            {
                "a": np.array([0, 1, 2, 3, 4, 5]),
            },
            {
                "p_id": np.array([0, 1, 2, 3, 4, 5]),
                "a": np.array([0, 1, 2, 3, 4, 5]),
            },
        ),
        # p_id and nested array updated
        (
            {
                "p_id": np.array([0, 1, 2]),
                "a": {"b": np.array([0, 1, 2])},
            },
            {
                "a": {"b": np.array([0, -1, 3, -1, 5, -1])},
            },
            {
                "p_id": np.array([0, 1, 2, 3, 4, 5]),
                "a": {"b": np.array([0, -1, 3, -1, 5, -1])},
            },
        ),
        # nested array updated with grouping variable broadcasted
        (
            {
                "a": {"b": np.array([0, 1, 2])},
                "c_id": np.array([0, 2, 2]),
            },
            {
                "a": {"b": np.array([0, 1, 2, 3, 4, 5])},
            },
            {
                "a": {"b": np.array([0, 1, 2, 3, 4, 5])},
                "c_id": np.array([0, 2, 2, 3, 5, 5]),
            },
        ),
        # nested array updated with foreign key broadcasted
        (
            {
                "a": {"b": np.array([0, 1, 2])},
                "c_p_id_d": np.array([0, -1, 2]),
            },
            {
                "a": {"b": np.array([0, 1, 2, 3, 4, 5])},
            },
            {
                "a": {"b": np.array([0, 1, 2, 3, 4, 5])},
                "c_p_id_d": np.array([0, -1, 2, 3, -1, 5]),
            },
        ),
        # nested array inserted with standard array broadcasted
        (
            {
                "a": {"b": np.array([0, 1, 2])},
                "c": np.array([True, False, True]),
            },
            {
                "a": {"b": np.array([0, 1, 2, 3, 4, 5])},
            },
            {
                "a": {"b": np.array([0, 1, 2, 3, 4, 5])},
                "c": np.array([True, False, True, True, False, True]),
            },
        ),
    ],
)
def test_upsert_input_data(data_from_persona, data_to_upsert, expected_upserted_data):
    upserted_data = upsert_input_data(data_from_persona, data_to_upsert)
    flat_upserted_data = dt.flatten_to_tree_paths(upserted_data)
    flat_expected_upserted_data = dt.flatten_to_tree_paths(expected_upserted_data)

    assert set(flat_upserted_data.keys()) == set(flat_expected_upserted_data.keys())

    for key in flat_upserted_data:
        assert np.array_equal(flat_upserted_data[key], flat_expected_upserted_data[key])


def test_upsert_input_data_fails_if_upserted_data_is_not_dict():
    data_from_persona = {
        "p_id": np.array([0, 1, 2]),
        "a": np.array([0, 1, 2]),
    }
    data_to_upsert = "not a dict"
    match = "data_to_upsert must be a dictionary."
    with pytest.raises(TypeError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)


def test_upsert_input_data_fails_if_data_to_upsert_is_not_dict_with_array_leafs():
    data_from_persona = {
        "p_id": np.array([0, 1, 2]),
        "a": np.array([0, 1, 2]),
    }
    data_to_upsert = {"a": "not a array"}
    match = "All leafs in data_to_upsert must be numpy Arrays or lists."
    with pytest.raises(TypeError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)


def test_upsert_input_data_fails_if_data_lengths_are_incompatible():
    data_from_persona = {
        "p_id": np.array([0, 1, 2]),
        "a": np.array([0, 1, 2]),
    }
    data_to_upsert = {
        "a": np.array([0, 1, 2, 3, 4]),
    }
    match = "The length of data in data_to_upsert is not a multiple"
    with pytest.raises(ValueError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)


def test_upsert_input_data_fails_if_length_of_data_in_to_upsert_different():
    data_from_persona = {
        "p_id": np.array([0, 1, 2]),
        "a": np.array([0, 1, 2]),
    }
    data_to_upsert = {
        "a": np.array([0, 1, 2, 3, 4]),
        "b": np.array([0, 1, 2, 3]),
    }
    match = "The length of data in data_to_upsert differ"
    with pytest.raises(ValueError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)
