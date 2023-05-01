import os
from paux.exception import ParamException


# 展开文件夹，获取里面的文件路径
def list_dirpath(dirpath: str, type='all', suffix='') -> list:
    '''
    :param dirpath: 文件夹地址
    :param type: 类型
        'all' 全部
        'dir' 文件夹
        'file' 文件
    :param suffix: 后缀
    '''
    type = type.lower()
    if type not in ['all', 'dir', 'file']:
        raise ParamException('type must in ["all","dir","file"]')

    filepaths = []
    for fn in os.listdir(dirpath):
        fp = os.path.join(dirpath, fn)
        if type == 'all':
            pass
        elif type == 'dir':
            if not os.path.isdir(fp):
                continue
        elif type == 'file':
            if os.path.isdir(fp):
                continue
        if not fn.endswith(suffix):
            continue
        filepaths.append(fp)
    return filepaths


# 获取文件夹中子孙文件名
def get_deep_filenames(dirpath: str, suffix: str = '') -> list:
    '''
    :param dirpath: 文件夹路径
    :param suffix: 后缀
    '''
    result_filenames = []
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        # 文件夹
        if os.path.isdir(filepath):
            result_filenames += get_deep_filenames(filepath, suffix)
        # 文件，并且后缀满足
        elif filepath.endswith(suffix):
            result_filenames.append(filename)
    return result_filenames


# 获取文件夹中子孙文件路径
def get_deep_filepaths(dirpath, suffix=''):
    '''
    :param dirpath: 文件夹路径
    :param suffix: 后缀
    '''
    result_filepaths = []
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        # 文件夹
        if os.path.isdir(filepath):
            result_filepaths += get_deep_filepaths(filepath, suffix)
        # 文件，并且后缀满足
        elif filepath.endswith(suffix):
            result_filepaths.append(filepath)
    return result_filepaths


if __name__ == '__main__':
    pass
    # print(list_dirpath('../dist', type='file', suffix='.whl'))
    # print(get_deep_filenames('../build', suffix=''))
    # print(get_deep_filepaths('../build', suffix='py'))
