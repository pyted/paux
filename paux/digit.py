# 保存源字符串的浮点数
class origin_float(float):
    def __init__(self, text: str):
        self.__text = text

    def origin(self):
        return self.__text


# 保存源字符串的整数
class origin_int(int):
    def __init__(self, text: str):
        self.__text = text

    def origin(self):
        return self.__text