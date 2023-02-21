import numpy as np
import pandas as pd
from collections.abc import Iterable
from copy import deepcopy


# 用于将函数中的局部变量变成字典
def to_local(data: dict, filter_keys=['self', '__class__']) -> dict:
    local_data = {}
    for k, v in data.items():
        if k not in filter_keys:
            local_data[k] = v
    return local_data


# 判断是否为空
def isnull(obj):
    '''
    :param obj: 支持类型有：Array、DataFrame、Series、Int、Float、Other
    :return:
    '''
    # Array
    if isinstance(obj, np.ndarray):
        return not obj.any()
    # DataFrame
    elif isinstance(obj, pd.DataFrame):
        return True if obj.shape[0] == 0 else False
    # Series
    elif isinstance(obj, pd.Series):
        return True if obj.shape[0] == 0 else False
    # Int|Float
    elif isinstance(obj, int) or isinstance(obj, float):
        if pd.isnull(obj):
            return True
        else:
            return False
    # Other
    else:
        return not bool(obj)


# 获取组合参数
def get_params(**kwargs) -> list:
    kwds = []
    for key in kwargs.keys():
        kwds.append({'key': key, 'value': kwargs[key]})

    def _func(kwds, params=[]):
        key = kwds[0]['key']
        values = kwds[0]['value']
        if not params:
            for value in values:
                params.append(
                    {key: value}
                )
        else:
            params2 = []
            if not isinstance(values, Iterable):
                values = [values, ]
            for value in values:
                for param in params:
                    this_param = deepcopy(param)
                    this_param[key] = value
                    params2.append(this_param)
            params = params2
        del kwds[0]
        if len(kwds) > 0:
            return _func(kwds, params=params)
        else:
            return params

    return _func(kwds=kwds)
