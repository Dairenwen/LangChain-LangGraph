"""租房查询中城市名称的标准化与中英文别名映射。"""


# 演示数据库中的国内城市及其英文别名。
#
# 这里采用“手动映射”：由代码明确维护每个城市的中文、英文对应关系，
# 而不是让大模型自行翻译城市名。这样可以审查、测试，也能避免模型把“武汉”
# 只转换为 "Wuhan"，导致无法匹配数据库中存储的“武汉”。
_CITY_TERMS = (
    ("北京", "Beijing"),
    ("上海", "Shanghai"),
    ("广州", "Guangzhou"),
    ("深圳", "Shenzhen"),
    ("成都", "Chengdu"),
    ("杭州", "Hangzhou"),
    ("武汉", "Wuhan"),
    ("南京", "Nanjing"),
    ("苏州", "Suzhou"),
    ("天津", "Tianjin"),
    ("重庆", "Chongqing"),
    ("西安", "Xi'an"),
    ("郑州", "Zhengzhou"),
    ("长沙", "Changsha"),
    ("青岛", "Qingdao"),
    ("宁波", "Ningbo"),
    ("无锡", "Wuxi"),
    ("福州", "Fuzhou"),
    ("厦门", "Xiamen"),
    ("济南", "Jinan"),
)

_CITY_LOOKUP = {
    alias.casefold(): terms
    for terms in _CITY_TERMS
    for alias in terms
}


# 演示房源只保存到区/县粒度，部分用户输入则是商圈或地铁站名。
# 手动维护这些“精细地点 -> 数据库行政区”的映射，避免把地点名直接与
# region_name 做等值比较而得到空结果。街道口位于武昌与洪山交界的生活圈，
# 因此两个区都会作为可审查的候选范围参与检索。
_DISTRICT_TERMS = {
    ("武汉", "街道口"): ("街道口", "武昌区", "洪山区"),
}


def strip_city_suffix(city: str) -> str:
    """去除仅用于展示的“市”或英文 ``City`` 后缀。"""
    normalized = city.strip()
    if normalized.endswith("市"):
        return normalized.removesuffix("市").strip()
    if normalized.casefold().endswith(" city"):
        return normalized[:-5].strip()
    return normalized


def city_search_terms(city: str) -> list[str]:
    """将中英文城市输入转换为数据库应同时检索的城市值。"""
    normalized = strip_city_suffix(city)
    if normalized == "随机城市":
        return []
    return list(_CITY_LOOKUP.get(normalized.casefold(), (normalized,)))


def normalized_city_name(city: str) -> str:
    """返回写入应用状态的标准城市名，优先使用映射中的中文名。"""
    terms = city_search_terms(city)
    return terms[0] if terms else strip_city_suffix(city)


def sql_city_predicate(city: str) -> str | None:
    """生成 SQL 查询必须使用的只读城市筛选条件。"""
    terms = city_search_terms(city)
    if not terms:
        return None
    quoted_terms = ", ".join("'" + term.replace("'", "''") + "'" for term in terms)
    return f"city_name IN ({quoted_terms})"


def district_search_terms(city: str, district: str) -> list[str]:
    """将商圈、街道等输入扩展为数据库中可用的区/县候选值。"""
    normalized_district = district.strip()
    # 用户常说“街道口附近/周边”，数据库映射表则维护地点本名。
    for suffix in ("附近", "周边"):
        if normalized_district.endswith(suffix):
            normalized_district = normalized_district.removesuffix(suffix).strip()
            break
    if not normalized_district or normalized_district in {"不限", "不限区域", "取消区域"}:
        return []
    normalized_city = normalized_city_name(city)
    return list(_DISTRICT_TERMS.get(
        (normalized_city, normalized_district),
        (normalized_district,),
    ))


def sql_district_predicate(city: str, district: str) -> str | None:
    """生成区域查询必须使用的 SQL 谓词；未限制区域时返回 ``None``。"""
    terms = district_search_terms(city, district)
    if not terms:
        return None
    quoted_terms = ", ".join("'" + term.replace("'", "''") + "'" for term in terms)
    return f"region_name IN ({quoted_terms})"
