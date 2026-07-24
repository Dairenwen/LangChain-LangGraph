import pytest

from agent.common.city_aliases import (
    city_search_terms,
    district_search_terms,
    normalized_city_name,
    sql_city_predicate,
    sql_district_predicate,
    strip_city_suffix,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("武汉市", "武汉"),
        (" 武汉市 ", "武汉"),
        ("Wuhan City", "Wuhan"),
        ("武汉", "武汉"),
    ],
)
def test_strip_city_suffix(value: str, expected: str):
    assert strip_city_suffix(value) == expected


@pytest.mark.parametrize("value", ["武汉", "武汉市", "Wuhan", "Wuhan City"])
def test_wuhan_aliases_search_both_languages(value: str):
    assert city_search_terms(value) == ["武汉", "Wuhan"]
    assert normalized_city_name(value) == "武汉"
    assert sql_city_predicate(value) == "city_name IN ('武汉', 'Wuhan')"


def test_unknown_city_only_uses_normalized_input():
    assert city_search_terms("洛阳市") == ["洛阳"]
    assert sql_city_predicate("洛阳市") == "city_name IN ('洛阳')"


def test_wuhan_jiedaokou_expands_to_available_districts():
    assert district_search_terms("武汉市", "街道口") == ["街道口", "武昌区", "洪山区"]
    assert district_search_terms("武汉市", "街道口附近") == ["街道口", "武昌区", "洪山区"]
    assert sql_district_predicate(
        "Wuhan", "街道口"
    ) == "region_name IN ('街道口', '武昌区', '洪山区')"


def test_unlimited_district_does_not_add_a_sql_predicate():
    assert district_search_terms("武汉", "不限区域") == []
    assert sql_district_predicate("武汉", "不限区域") is None
