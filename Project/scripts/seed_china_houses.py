#!/usr/bin/env python3
"""Generate deterministic demo rental listings for major Chinese cities.

The script writes SQL to stdout so it can be reviewed or piped to the MySQL
client.  It deliberately does not store any database credentials.
"""

from __future__ import annotations

from decimal import Decimal


# Four first-tier cities and sixteen representative second-tier cities.
# Each tuple contains city id, name, districts, centre longitude/latitude, and
# a reasonable monthly rent range in CNY for the demo data.
CITIES = (
    (201, "北京", ("海淀区", "朝阳区", "西城区", "丰台区"), 116.4074, 39.9042, 4200, 10500),
    (202, "上海", ("浦东新区", "徐汇区", "静安区", "杨浦区"), 121.4737, 31.2304, 4500, 11000),
    (203, "广州", ("天河区", "越秀区", "海珠区", "番禺区"), 113.2644, 23.1291, 3000, 7600),
    (204, "深圳", ("南山区", "福田区", "龙华区", "宝安区"), 114.0579, 22.5431, 3800, 9000),
    (205, "成都", ("武侯区", "锦江区", "高新区", "成华区"), 104.0665, 30.5728, 1800, 4600),
    (206, "杭州", ("西湖区", "滨江区", "余杭区", "拱墅区"), 120.1551, 30.2741, 2600, 6400),
    (207, "武汉", ("武昌区", "洪山区", "江汉区", "汉阳区"), 114.3054, 30.5931, 1600, 4000),
    (208, "南京", ("建邺区", "鼓楼区", "玄武区", "江宁区"), 118.7969, 32.0603, 2400, 5900),
    (209, "苏州", ("工业园区", "姑苏区", "吴中区", "高新区"), 120.5853, 31.2989, 2300, 5600),
    (210, "天津", ("和平区", "南开区", "河西区", "西青区"), 117.2000, 39.1333, 1700, 4300),
    (211, "重庆", ("渝中区", "江北区", "南岸区", "沙坪坝区"), 106.5516, 29.5630, 1500, 3800),
    (212, "西安", ("雁塔区", "碑林区", "未央区", "高新区"), 108.9398, 34.3416, 1500, 3700),
    (213, "郑州", ("金水区", "中原区", "郑东新区", "二七区"), 113.6254, 34.7466, 1400, 3400),
    (214, "长沙", ("岳麓区", "芙蓉区", "雨花区", "开福区"), 112.9388, 28.2282, 1400, 3500),
    (215, "青岛", ("市南区", "市北区", "崂山区", "李沧区"), 120.3826, 36.0671, 1800, 4500),
    (216, "宁波", ("鄞州区", "海曙区", "江北区", "北仑区"), 121.5440, 29.8683, 1800, 4300),
    (217, "无锡", ("滨湖区", "梁溪区", "新吴区", "惠山区"), 120.3119, 31.4912, 1700, 4100),
    (218, "福州", ("鼓楼区", "台江区", "仓山区", "晋安区"), 119.2965, 26.0745, 1700, 4100),
    (219, "厦门", ("思明区", "湖里区", "集美区", "海沧区"), 118.0894, 24.4798, 2300, 5600),
    (220, "济南", ("历下区", "市中区", "槐荫区", "历城区"), 117.1201, 36.6512, 1500, 3600),
)

ROOMS = ("1室1厅1卫", "2室1厅1卫", "2室2厅1卫", "3室1厅1卫", "3室2厅2卫")
ORIENTATIONS = ("南", "南北", "东南", "西南", "东")
DEVICES = (
    "空调,冰箱,洗衣机,热水器,衣柜",
    "空调,冰箱,洗衣机,燃气灶,油烟机",
    "空调,热水器,宽带,电梯,衣柜",
    "空调,冰箱,洗衣机,阳台,可做饭",
)


def sql(value: object) -> str:
    """Return a MySQL literal, escaping only values generated in this file."""
    if value is None:
        return "NULL"
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def listing_rows() -> list[tuple[object, ...]]:
    rows: list[tuple[object, ...]] = []
    serial = 1
    for city_id, city, districts, longitude, latitude, price_min, price_max in CITIES:
        for index in range(50):
            district = districts[index % len(districts)]
            room = ROOMS[index % len(ROOMS)]
            rent_type = "整租" if index % 5 else "合租"
            house_type = "住宅" if index % 4 else "公寓"
            floor = index % 24 + 1
            all_floor = max(floor, 12 + index % 22)
            area = Decimal("38.00") + Decimal((index * 13 + city_id) % 105) + Decimal(".50")
            price = price_min + ((index * 211 + city_id * 17) % (price_max - price_min + 1))
            community = f"{district}安居花园{index // len(districts) + 1}期"
            title = f"{city}{district}{room}精装{rent_type}{index + 1:02d}"
            intro = (
                f"{city}{district}优质{rent_type}房源，{room}，采光良好，"
                "邻近地铁与生活配套，适合长期居住。"
            )
            rows.append((
                200000 + serial,
                title,
                rent_type,
                floor,
                all_floor,
                house_type,
                room,
                ORIENTATIONS[index % len(ORIENTATIONS)],
                area,
                price,
                intro,
                DEVICES[index % len(DEVICES)],
                f"https://picsum.photos/seed/cn-house-{serial:04d}/640/480",
                f"https://picsum.photos/seed/cn-house-{serial:04d}/1200/800",
                city_id,
                city,
                city_id * 1000 + index % len(districts) + 1,
                district,
                community,
                f"{city}{district}{community}{index + 1}号",
                Decimal(str(longitude)) + Decimal(index % 10) / Decimal("1000"),
                Decimal(str(latitude)) + Decimal(index // 10) / Decimal("1000"),
            ))
            serial += 1
    return rows


def main() -> None:
    columns = (
        "user_id", "title", "rent_type", "floor", "all_floor", "house_type", "rooms",
        "position", "area", "price", "intro", "devices", "head_image", "images", "city_id",
        "city_name", "region_id", "region_name", "community_name", "detail_address", "longitude", "latitude",
    )
    rows = listing_rows()
    assert len(rows) == 1000
    print("START TRANSACTION;")
    print(f"INSERT INTO house ({', '.join(columns)}) VALUES")
    for index, row in enumerate(rows):
        suffix = ";" if index == len(rows) - 1 else ","
        print("(" + ", ".join(sql(value) for value in row) + ")" + suffix)
    print("COMMIT;")


if __name__ == "__main__":
    main()
