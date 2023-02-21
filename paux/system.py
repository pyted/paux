import os
import platform
from paux import exception


# 获得平台名称
def get_platform() -> str:
    '''
    :return: WINDOWS | MACOS | LINUX | OTHER
    '''
    sys_platform = platform.platform().upper()
    sys_names = (
        'WINDOWS', 'MACOS', 'LINUX'
    )
    for sys_name in sys_names:
        if sys_name in sys_platform:
            return sys_name
    return 'OTHER'


# 获取macOs用户的文稿文件位置
def get_maxOs_documents_path() -> str:
    root_path = '/Users'
    filepaths = []
    for filename in os.listdir(root_path):
        if filename.startswith('.'):
            continue
        if filename == 'Shared':
            continue
        filepath = os.path.join(root_path, filename)
        if os.path.isdir(filepath) and 'Documents' in os.listdir(filepath):
            filepaths.append(filepath)

    if not filepaths:
        msg = 'Unable to get MacOs username path'
        raise exception.ExecuteException(msg)
    documents_path = os.path.join(
        filepaths[0], 'Documents'
    )
    return documents_path