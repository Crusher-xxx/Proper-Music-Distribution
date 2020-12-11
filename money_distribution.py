from decimal import Decimal, ROUND_HALF_DOWN


def distribution_income(musician__listening_time, subscription_price):
    # Если список пуст, то вернуть пустой список
    if not musician__listening_time:
        return {}

    # Рассчитать сколько денег приходится на одну единицу времени
    total_listening_time = sum(musician__listening_time.values())
    coefficient = Decimal(subscription_price / total_listening_time)
    coefficient = coefficient.quantize(Decimal("1.000000000"), ROUND_HALF_DOWN)

    # Распределить деньги
    musician_share = {}
    for musician in musician__listening_time:
        musician_share[musician] = musician__listening_time[musician] * coefficient
        musician_share[musician] = musician_share[musician].quantize(Decimal("1.00"), ROUND_HALF_DOWN)

    # Забрать перерасход у богатейшего или отдать ему остаток
    richest = max(musician_share, key=musician_share.get)
    musician_share[richest] += subscription_price - sum(musician_share.values())

    for key in musician_share:
        musician_share[key] = musician_share[key]
    return musician_share