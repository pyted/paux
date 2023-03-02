from typing import Literal, Union
from paux import exception
import re


# 计算手续费
def get_commission_data(
        posSide: Literal['long', 'short', 'LONG', 'SHORT'],
        openMoney: Union[int, float],
        openPrice: Union[int, float],
        closePrice: Union[int, float],
        lever: Union[int, float],
        openCommissionRate: Union[int, float],
        closeCommissionRate: Union[int, float]
) -> dict:
    '''
    :param posSide: 持仓方向
        LONG:   多单
        SHORT:  空单
    :param openMoney: 开仓金额
    :param openPrice: 开仓价格
    :param closePrice: 平仓价格
    :param lever: 杠杆倍数
    :param openCommissionRate: 开仓手续费率
    :param closeCommissionRate: 平仓手续费率
    :return
        {
            'closeMoney' : <平仓剩余金额>, # 保留4个小数位
            'commission' : <开仓与平仓手续费之和>, # 保留4个小数位
            'profitRate' : <利润率>, # 保留4个小数位
        }
    '''
    if posSide.upper() == 'LONG':
        buyCommission = openMoney * lever * openCommissionRate
        sellCommission = (closePrice / openPrice) * openMoney * lever * closeCommissionRate
        commission = round(buyCommission + sellCommission, 4)
        closeMoney = round((closePrice - openPrice) / openPrice * lever * openMoney + openMoney - commission, 4)
        profitRate = round((closeMoney - openMoney) / openMoney, 4)
        return dict(
            closeMoney=closeMoney,
            commission=commission,
            profitRate=profitRate,
        )
    elif posSide.upper() == 'SHORT':
        buyCommission = openMoney * lever * openCommissionRate
        sellCommission = (2 * openPrice - closePrice) / openPrice * openMoney * lever * closeCommissionRate
        commission = round(buyCommission + sellCommission, 4)
        closeMoney = (openPrice - closePrice) / openPrice * openMoney * lever + openMoney - commission
        profitRate = round((closeMoney - openMoney) / openMoney, 4)
        return dict(
            closeMoney=closeMoney,
            commission=commission,
            profitRate=profitRate,
        )


# 用于模拟交易中的的价格圆整，保证圆整后的价格与圆整前相差不超过0.001%
def round_simulate(price) -> float:
    '''
    :param price: 价格
    '''
    if isinstance(price, int):
        return price
    if price == 0:
        return price
    price_0_00001 = 0.00001 * price
    if price_0_00001 < 1:
        ndigits = len(str(int(1 / price_0_00001)))
        price_round = round(price, ndigits)
    else:
        price_round = round(price, 1)
    if abs((price_round - price) / price) >= 0.00001:
        msg = f'price_round={price_round},price={price}'
        raise exception.ExecuteException(msg)
    else:
        return price_round


# 圆整购买数量
def round_quantity(
        quantity,
        stepSize: str,
        minQty: str = None,
        maxQty: str = None
):
    '''
    :param quantity: 输入数量
    :param stepSize: 购买数量的最小间隔
    :param minQty: 数量下限, 最小数量   None:无下限
    :param maxQty: 数量上限, 最大数量   None:无上限
    :return
        格式:
            {
                'code' : <int>,
                'data' : <int|float:quantity>,
                'msg' : <str>
            }
        code:
            0     属于 minQty~maxQty之间
            -1    小于minQty
            -2    大于maxQty
    '''

    # 数字对象
    if quantity / float(stepSize) == int(quantity / float(stepSize)):
        quantity = quantity
    else:
        quantity = quantity // float(stepSize) * float(
            stepSize)  # quantity = 52.123 stepSize = 0.01 --> quantity = 52.1
    if '.' in stepSize:
        stepSize = re.sub('0+$', '', stepSize)
        m = len(stepSize.split('.', maxsplit=1)[-1])  # 小数位
        quantity = round(quantity, m)
    else:
        quantity = int(quantity)
    result = {
        'code': 0,
        'data': quantity,
        'msg': ''
    }
    if minQty and quantity < float(minQty):
        result['code'] = -1
        result['msg'] = f'quantity={quantity} minQty={minQty}'
    elif maxQty and quantity > float(maxQty):
        result['code'] = -2
        result['msg'] = f'quantity={quantity} maxQty={maxQty}'
    return result


# 圆整购买价格
def round_price(
        price,
        type: Literal['CEIL', 'FLOOR', 'ceil', 'floor'],
        tickSize,
        minPrice: str = None,
        maxPrice: str = None,

):
    '''
    :param price: 购买价格
    :param type: 圆整方式
        CEIL:   向上圆整
        FLOOR:  向下圆整
    :param tickSize: 价格的最小间隔
    :param minPrice: 最小价格
    :param maxPrice: 最大价格
    :return:
        格式：
            {
                'code' : <int>,
                'data' : <int|float:quantity>,
                'msg' : <str>
            }
        code:
            0     属于 minPrice~maxPrice之间
            -1    小于minPrice
            -2    大于maxPrice
    '''
    # 向下或向上圆整
    type = type.upper()
    if type not in ['CEIL', 'FLOOR']:
        msg = 'type must in ["CEIL","FLOOR"]'
        raise exception.ParamException(msg)
    if price / float(tickSize) == int(price / float(tickSize)):
        price = price
    else:
        if type == 'CEIL':
            price = (price // float(tickSize) + 1) * float(tickSize)  # price = 52.123 tickSize = 0.01 --> price = 52.2
        else:
            price = price // float(tickSize) * float(tickSize)  # price = 52.123 tickSize = 0.01 --> price = 52.1

    if '.' in tickSize:
        tickSize = re.sub('0+$', '', tickSize)
        m = len(tickSize.split('.', maxsplit=1)[-1])  # 小数位
        price = round(price, m)
    else:
        price = int(price)

    result = {
        'code': 0,
        'data': price,
        'msg': ''
    }
    if minPrice and price < float(minPrice):
        result['code'] = -1
        result['msg'] = f'price={price} minPrice={minPrice}'
    elif maxPrice and price > float(maxPrice):
        result['code'] = -2
        result['msg'] = f'price={price} maxPrice={maxPrice}'
    return result


# 根据开仓金额、开仓价格、杠杆获取可以开仓的数量
def get_quantity(
        openPrice: Union[int, float],
        openMoney: Union[int, float],
        stepSize: str,
        lever: int = 1,
        minQty: str = None,
        maxQty: str = None
):
    '''
    :param openPrice: 开仓价格
    :param openMoney: 开仓金额
    :param stepSize: 购买数量的最小间隔
    :param lever: 杠杆倍数
    :param minQty: 数量下限, 最小数量   None:无下限
    :param maxQty: 数量上限, 最大数量   None:无上限
    :return: 结果同round_quantity
    '''
    quantity = openMoney * lever / openPrice
    result = round_quantity(
        quantity=quantity,
        stepSize=stepSize,
        minQty=minQty,
        maxQty=maxQty,
    )
    return result


# 将开仓数量转化为字符串
def quantity_to_f(
        quantity: Union[int, float],
        stepSize: str
):
    '''
    :param quantity: 开仓数量
    :param stepSize: 购买数量的最小间隔
    :return:
        格式：
            {
                'code' : <int>,
                'data' : <str:quantity_f>,
                'msg' : <str>
            }
        code:
            0   正确
            -1  转换后字符串格式quantity与数字格式quantity不相等
    '''
    # m 小数位
    if float(stepSize) >= 1:
        m = 0
    else:
        stepSize = re.sub('0+$', '', stepSize)
        m = len(stepSize.split('.', maxsplit=1)[-1])
    d_format = '%.{m}f'.format(m=m)
    quantity_f = d_format % quantity
    if float(quantity_f) != quantity:
        result = {
            'code': -1,
            'data': quantity_f,
            'msg': f'quantity_f != quantity quantity = {quantity} quantity_f = {quantity_f}',
        }
    else:
        result = {
            'code': 0,
            'data': quantity_f,
            'msg': ''
        }
    return result


# 将开仓价格转化为字符串
def price_to_f(
        price: Union[int, float],
        tickSize: str
):
    '''
    :param quantity: 开仓价格
    :param tickSize: 价格的最小间隔
    :return:
        格式：
            {
                'code' : <int>,
                'data' : <str:price_f>,
                'msg' : <str>
            }
        code:
            0   正确
            -1  转换后字符串格式price与数字格式price不相等
    '''
    # m 小数位
    if float(tickSize) >= 1:
        m = 0
    else:
        tickSize = re.sub('0+$', '', tickSize)
        m = len(tickSize.split('.', maxsplit=1)[-1])
    d_format = '%.{m}f'.format(m=m)
    price_f = d_format % price
    if float(price_f) != price:
        result = {
            'code': -1,
            'data': price_f,
            'msg': f'price_f != price price= {price} price_f= {price_f}',
        }
    else:
        result = {
            'code': 0,
            'data': price_f,
            'msg': ''
        }
    return result
