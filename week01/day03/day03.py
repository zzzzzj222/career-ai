'''
'''

# from my_module import file_read

# file_read()

def str_reverse(s):
    # 将字符串反转
    return s[::-1]


print(str_reverse('abc'))

'''
优惠卷金额需要满5000才可以使用，优惠卷金额不能超过商品总价
积分抵扣需要满5000才可以使用，100积分抵扣1元，积分抵扣金额不能超过商品总价，只能整百抵扣
'''

def calc_order_cost(*args: tuple[str, float, int], coupon: float, score: float, express: float) -> float:
    """
    计算订单总价
    :param args: 商品信息（商品名、价格、数量）
    :param coupon: 优惠券金额
    :param score: 积分抵扣金额
    :param express: 运费
    :return: 订单总价
    """
    total_price = [goods[1] * goods[2] for goods in args]
    total_cost = sum(total_price)

    if total_cost >= 5000 and coupon <= total_cost:
        total_cost -= coupon
# //代表整除
    if total_cost >= 5000 and score // 100 <= total_cost:  
        total_cost -= (score // 100)  # 积分抵扣金额只能整百抵扣

    total_cost += express
    return total_cost


# 可变参数后需要使用关键字参数传递优惠券金额、积分抵扣金额和运费，否则可变参数需要放在最后
res=calc_order_cost(('商品1', 1000, 3), ('商品2', 2000, 2), coupon=500.0, score=300.0, express=9.9)
print(f"订单总价: {res}")