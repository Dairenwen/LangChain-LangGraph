from langgraph.graph import MessagesState
# 推荐子图的状态

# 推荐房源状态
class RecommendState(MessagesState):
    # 用户偏好，与主图数据共享
    user_preferences: dict
    # 以下是推荐的关键参数
    city: str          # 城市
    city_search_terms: list[str]  # 城市在数据库中的中英文检索值
    district_search_terms: list[str]  # 区域、商圈等输入展开后的数据库检索值
    recommendation_found: bool  # 最近一次数据库检索是否实际返回房源
    search_cancelled: bool  # 用户在无结果追问中主动结束检索
    budget_min: float  # 最低预算
    budget_max: float  # 最高预算
    district: str      # 区域
    room_type: str     # 房屋类型
    orientation: str   # 朝向
    room_count: int    # 推荐数量
    others: str        # 其它要求

# 获取推荐信息方法
def get_recommend_info(state: dict) -> str:
    info_prompt = """
提取用户期望推荐的房源信息如下:
- 城市: {city}
- 城市 SQL 检索候选值（必须原样用于 city_name 检索，不能翻译或改写）: {city_search_terms}
- 区域: {district}
- 预算: {budget_min} - {budget_max} 元/月
- 房屋类型: {room_type}
- 朝向: {orientation}
- 特殊要求: {others}
- 推荐数量: {room_count}
如果某些信息未指定，请使用合适的默认值或放宽条件。"""
    return info_prompt.format(
        city=state.get('city', '未指定'),
        city_search_terms=state.get('city_search_terms', []),
        district=state.get('district', '未指定'),
        budget_min=state.get('budget_min', '未指定'),
        budget_max=state.get('budget_max', '未指定'),
        room_type=state.get('room_type', '未指定'),
        orientation=state.get('orientation', '未指定'),
        others=state.get('others', '无'),
        room_count=state.get('room_count', 5)
    )
