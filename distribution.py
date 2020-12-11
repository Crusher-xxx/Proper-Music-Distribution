from decimal import Decimal, ROUND_HALF_DOWN


def distribution_income(listen_time, sub_money):
    total_time_listen = sum(listen_time.values())
    print("Total time listen=", total_time_listen)

    koef = Decimal(sub_money / total_time_listen)
    koef = koef.quantize(Decimal("1.0000000"), ROUND_HALF_DOWN)
    print("Coefficient in one unit=", koef)

    mus_shape = {}
    for key in listen_time:
        mus_shape[key] = listen_time[key] * koef
        mus_shape[key] = mus_shape[key].quantize(Decimal("1.00"), ROUND_HALF_DOWN)
    # print(mus_shape)
    return mus_shape


# N = int(input("Сколько всего музыкантов: "))
# quantity_musicians = list(range(N))
# print(quantity_musicians)
#
# M = int(input("Сколько музыкантов он слушает: "))
# musicians_listen_time = {}
# for _ in range(M):
#     print(_ + 1, ')Id Музыканта которого слушает:')
#     quantity_musicians_listen = int(input())
#     print("Музыканта", quantity_musicians_listen, "слушает (по времени): ")
#     quantity_musicians_listen_time = int(input())
#     musicians_listen_time[quantity_musicians_listen] = quantity_musicians_listen_time
#
# print(musicians_listen_time)
#
# print("Месячная подписка:")
# sub = float(input())
#
# musicians_shape = distribution_income(musicians_listen_time, sub)
#
# print(musicians_shape)
#
# zzz = sum(musicians_shape.values())  # check mus_shape and sub (= or not)
# print(zzz)

import random
if __name__ == '__main__':
    money = 150
    lst_tim = {'0': 23, '1': 45, '2': 156, '3': 46, '4': 156, '5': 2, '6': 1, '7': 1, '8': 1024, '9': 57}
    min = 0; max = 5000
    lst_tim = {'0': random.randint(min, max), '1': random.randint(min, max), '2': random.randint(min, max),
               '3': random.randint(min, max), '4': random.randint(min, max), '5': random.randint(min, max),
               '6': random.randint(min, max), '7': random.randint(min, max), '8': random.randint(min, max),
               '9': random.randint(min, max)}
    dst = distribution_income(lst_tim, money)

    sum = 0
    for x in dst.values():
        sum += x
    print(sum)
    print(dst)
    print(lst_tim)

