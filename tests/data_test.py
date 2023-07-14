from allib.data import merge_dicts, update_dict


def test_simple_dict_merge_does_not_modify_existing_dicts():
    d1 = {"a": "a"}
    d2 = {"b": "b"}
    merged = merge_dicts(d1, d2)
    assert {"a": "a"} == d1
    assert {"b": "b"} == d2
    assert {"a": "a", "b": "b"} == merged


def test_merge_dicts():
    d1 = {"a": {"b": {"c": "d"}}}
    d2 = {"a": {"b": {"c": "e"}}}
    merged = merge_dicts(d1, d2)
    assert "d" == d1["a"]["b"]["c"]
    assert "e" == merged["a"]["b"]["c"]


def test_update_dict():
    d1 = {"a": {"b": "c"}}
    d2 = {"a": {"b": "d", "e": "f"}}
    update_dict(d1, d2)
    assert {"a": {"b": "d", "e": "f"}} == d1
    assert {"a": {"b": "d", "e": "f"}} == d2
