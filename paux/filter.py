from typing import Union
import time


class Filter():
    def __init__(self):
        # 过滤内容，格式：
        # {
        #     '<name>':{
        #         'ts':<int>,
        #         'expire':<int>,
        #     },
        # }
        # 时间戳以秒为单位
        self.filter_map = {}

    # 设置过滤对象
    def set(
            self,
            name,
            filter_minute: Union[int, float] = 5
    ):
        '''
        :param name: 对象名称
        :param filter_minute: 缓存的分钟数
        '''
        ts = int(time.time())
        self.filter_map[name] = {
            'ts': ts,
            'expire': ts + filter_minute * 60
        }

    # 检查是否被过滤
    def check(self, name):
        '''
        :param name: 对象名称
        :return:
            True 不过滤
            False 过滤
        '''

        # 清除超过缓存的数据
        self.clear()
        # filter_map中仅保留未过期的缓存对象
        if not name in self.filter_map.keys():
            return True  # 不过滤
        else:
            return False  # 过滤

    # 清除过期的过滤对象
    def clear(self):
        this_time = time.time()
        remove_keys = []
        for key, data in self.filter_map.items():
            if this_time >= data['expire']:
                remove_keys.append(key)
        for key in remove_keys:
            del self.filter_map[key]
