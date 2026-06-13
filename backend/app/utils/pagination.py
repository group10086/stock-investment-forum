"""分页工具"""

from math import ceil


def paginate(query, page: int = 1, page_size: int = 10):
    """通用分页查询

    Args:
        query: SQLAlchemy query对象
        page: 页码，从1开始
        page_size: 每页数量

    Returns:
        (items, total, has_more)
    """
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    has_more = (offset + page_size) < total
    return items, total, has_more
