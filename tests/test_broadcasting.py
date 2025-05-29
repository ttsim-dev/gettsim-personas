import dags.tree as dt
import pandas as pd
import pytest

from gettsim_personas.broadcasting import (
    broadcast_foreign_keys,
    broadcast_group_ids,
    broadcast_p_id,
)
from gettsim_personas.interface import upsert_input_data


@pytest.mark.parametrize(
    (
        "p_id_series",
        "expected_length",
        "expected_p_id",
    ),
    [
        (pd.Series([0, 1, 2]), 3, [0, 1, 2]),
        (pd.Series([0, 1, 2]), 6, [0, 1, 2, 3, 4, 5]),
    ],
)
def test_broadcast_p_id(p_id_series, expected_length, expected_p_id):
    broadcasted_p_id = broadcast_p_id(p_id_series, expected_length)
    assert broadcasted_p_id.equals(pd.Series(expected_p_id))


def test_broadcasting_p_id_fails_if_p_id_is_not_consecutive():
    p_id_series = pd.Series([0, 2, 3])
    expected_length = 3
    with pytest.raises(ValueError, match="Persona p_id does not start with 0 or"):
        broadcast_p_id(p_id_series, expected_length)


def test_broadcasting_p_id_fails_if_p_id_is_not_starting_with_0():
    p_id_series = pd.Series([1, 2, 3])
    expected_length = 3
    with pytest.raises(ValueError, match="Persona p_id does not start with 0 or"):
        broadcast_p_id(p_id_series, expected_length)


@pytest.mark.parametrize(
    (
        "original_series",
        "expected_length",
        "expected_series",
    ),
    [
        (pd.Series([0, 1, 2]), 3, pd.Series([0, 1, 2])),
        (pd.Series([0, 1, 2]), 6, pd.Series([0, 1, 2, 3, 4, 5])),
        (pd.Series([0, 0, 0]), 6, pd.Series([0, 0, 0, 1, 1, 1])),
        (pd.Series([0, 3, 5]), 6, pd.Series([0, 3, 5, 6, 9, 11])),
    ],
)
def test_broadcast_series_with_group_or_foreign_keys(
    original_series, expected_length, expected_series
):
    broadcasted_series = broadcast_group_ids(original_series, expected_length)
    assert broadcasted_series.equals(pd.Series(expected_series))


@pytest.mark.parametrize(
    (
        "original_series",
        "expected_length",
        "expected_series",
    ),
    [
        (pd.Series([0, 1, 2]), 6, pd.Series([0, 1, 2, 3, 4, 5])),
        (pd.Series([-1, 0, 2]), 6, pd.Series([-1, 0, 2, -1, 3, 5])),
    ],
)
def test_broadcast_foreign_keys(original_series, expected_length, expected_series):
    broadcasted_series = broadcast_foreign_keys(original_series, expected_length)
    assert broadcasted_series.equals(pd.Series(expected_series))


@pytest.mark.parametrize(
    (
        "data_from_persona",
        "data_to_upsert",
        "expected_upserted_data",
    ),
    [
        # p_id and simple series updated
        (
            {
                "p_id": pd.Series([0, 1, 2]),
                "a": pd.Series([0, 1, 2]),
            },
            {
                "a": pd.Series([0, 1, 2, 3, 4, 5]),
            },
            {
                "p_id": pd.Series([0, 1, 2, 3, 4, 5]),
                "a": pd.Series([0, 1, 2, 3, 4, 5]),
            },
        ),
        # p_id and nested series updated
        (
            {
                "p_id": pd.Series([0, 1, 2]),
                "a": {"b": pd.Series([0, 1, 2])},
            },
            {
                "a": {"b": pd.Series([0, -1, 3, -1, 5, -1])},
            },
            {
                "p_id": pd.Series([0, 1, 2, 3, 4, 5]),
                "a": {"b": pd.Series([0, -1, 3, -1, 5, -1])},
            },
        ),
        # nested series updated with grouping variable broadcasted
        (
            {
                "a": {"b": pd.Series([0, 1, 2])},
                "c_id": pd.Series([0, 2, 2]),
            },
            {
                "a": {"b": pd.Series([0, 1, 2, 3, 4, 5])},
            },
            {
                "a": {"b": pd.Series([0, 1, 2, 3, 4, 5])},
                "c_id": pd.Series([0, 2, 2, 3, 5, 5]),
            },
        ),
        # nested series updated with foreign key broadcasted
        (
            {
                "a": {"b": pd.Series([0, 1, 2])},
                "c_p_id_d": pd.Series([0, -1, 2]),
            },
            {
                "a": {"b": pd.Series([0, 1, 2, 3, 4, 5])},
            },
            {
                "a": {"b": pd.Series([0, 1, 2, 3, 4, 5])},
                "c_p_id_d": pd.Series([0, -1, 2, 3, -1, 5]),
            },
        ),
        # nested series inserted with standard series broadcasted
        (
            {
                "a": {"b": pd.Series([0, 1, 2])},
                "c": pd.Series([True, False, True]),
            },
            {
                "a": {"b": pd.Series([0, 1, 2, 3, 4, 5])},
            },
            {
                "a": {"b": pd.Series([0, 1, 2, 3, 4, 5])},
                "c": pd.Series([True, False, True, True, False, True]),
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
        assert flat_upserted_data[key].equals(flat_expected_upserted_data[key])


def test_upsert_input_data_fails_if_upserted_data_is_not_dict():
    data_from_persona = {
        "p_id": pd.Series([0, 1, 2]),
        "a": pd.Series([0, 1, 2]),
    }
    data_to_upsert = "not a dict"
    match = "data_to_upsert must be a dictionary."
    with pytest.raises(TypeError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)


def test_upsert_input_data_fails_if_data_to_upsert_is_not_dict_with_series_leafs():
    data_from_persona = {
        "p_id": pd.Series([0, 1, 2]),
        "a": pd.Series([0, 1, 2]),
    }
    data_to_upsert = {"a": "not a series"}
    match = "All leafs in data_to_upsert must be pandas Series."
    with pytest.raises(TypeError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)


def test_upsert_input_data_fails_if_data_lengths_are_incompatible():
    data_from_persona = {
        "p_id": pd.Series([0, 1, 2]),
        "a": pd.Series([0, 1, 2]),
    }
    data_to_upsert = {
        "a": pd.Series([0, 1, 2, 3, 4]),
    }
    match = "The length of data in data_to_upsert is not a multiple"
    with pytest.raises(ValueError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)


def test_upsert_input_data_fails_if_length_of_data_in_to_upsert_different():
    data_from_persona = {
        "p_id": pd.Series([0, 1, 2]),
        "a": pd.Series([0, 1, 2]),
    }
    data_to_upsert = {
        "a": pd.Series([0, 1, 2, 3, 4]),
        "b": pd.Series([0, 1, 2, 3]),
    }
    match = "The length of data in data_to_upsert differ"
    with pytest.raises(ValueError, match=match):
        upsert_input_data(data_from_persona, data_to_upsert)
