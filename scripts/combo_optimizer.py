
from decimal import Decimal
from itertools import combinations


def find_combinations(items, budget, max_items=3, limit=10):
    """
    从已查询到的餐品中寻找不超预算的组合。

    items: [{"name": "餐品名称", "price": "25.5"}, ...]
    budget: 用户预算，例如 "60"
    max_items: 每组最多包含多少种餐品
    limit: 最多返回多少个组合

    注意：每种餐品在一个组合中最多出现一次。
    """
    budget = Decimal(str(budget))

    if budget < 0:
        raise ValueError("预算不能小于 0")
    if max_items < 1:
        raise ValueError("max_items 必须至少为 1")
    if limit < 1:
        raise ValueError("limit 必须至少为 1")

    normalized = []
    for item in items:
        name = str(item["name"]).strip()
        price = Decimal(str(item["price"]))

        if not name:
            raise ValueError("餐品名称不能为空")
        if price < 0:
            raise ValueError(f"餐品价格不能小于 0：{name}")

        normalized.append({"name": name, "price": price})

    results = []
    max_size = min(max_items, len(normalized))

    for size in range(1, max_size + 1):
        for group in combinations(normalized, size):
            total = sum(
                (item["price"] for item in group),
                Decimal("0")
            )

            if total <= budget:
                results.append({
                    "items": [item["name"] for item in group],
                    "total": total,
                    "remaining": budget - total,
                    "count": size,
                })

    # 优先展示最接近预算且不超预算的组合
    results.sort(
        key=lambda x: (
            -x["total"],
            -x["count"],
            x["items"],
        )
    )

    return results[:limit]


def main():
    # 以下是演示数据，不代表实时菜单或当前售价。
    sample_items = [
        {"name": "巨无霸", "price": "25.5"},
        {"name": "麦辣鸡腿汉堡", "price": "20.0"},
        {"name": "薯条", "price": "12.0"},
        {"name": "可乐", "price": "9.0"},
    ]

    budget = "40.0"
    results = find_combinations(
        sample_items,
        budget,
        max_items=3,
    )

    print(f"预算：{budget} 元")
    print("以下为演示数据计算结果：")

    for index, result in enumerate(results, start=1):
        names = " + ".join(result["items"])
        print(
            f"{index}. {names} | "
            f"合计 {result['total']:.2f} 元 | "
            f"剩余 {result['remaining']:.2f} 元"
        )


if __name__ == "__main__":
    main()
