from multiprocessing import Process, Manager
import traceback
import time
from paux import exception


# 进程工作者
def _pool_worker(q_param, q_result):
    '''
    :param q_param: 参数队列
    :param q_result: 结果队列
    '''
    while True:
        try:
            data = q_param.get(block=False, timeout=0)
            index = data['index']  # 索引
            param = data['param']  # 函数的执行参数
            skip_exception = data['skip_exception']  # 遇到异常不会终止工作器
            func = param['func']  # 函数
            del param['func']
        except:
            break
        if skip_exception:
            try:
                ret = func(**param)
                q_result.put(
                    {
                        'index': index,
                        'data': ret
                    }
                )
            except:
                print(traceback.format_exc())
        else:
            ret = func(**param)
            q_result.put(
                {
                    'index': index,
                    'data': ret
                }
            )


# 进程装饰器
def process_wrapper(func):
    def wrapper(*args, **kwargs):
        process_target = Process(target=func, args=args, kwargs=kwargs)
        process_target.run()
        return process_target

    return wrapper


def pool_worker(
        params,
        p_num=4,
        func=None,
        skip_exception=False
):
    '''
    :param params: 参数序列 [dict,dict....]
    :param p_num: 进程数
    :param func: 执行函数
        函数地址如果在params中，func可以为None
        优先级: params[<index>]['func'] >> func
    :param skip_exception: 子进程中出现异常是否终止
        True:   出现异常，报告错误信息，不会终止子进程
        False:  出现异常，终止子进程
    :return
        [result、result... ...]
    '''
    # 结果按照params的索引对应
    results = [None] * len(params)
    # 标准化param，让param中存在要执行的函数func
    q_param = Manager().Queue()  # 参数队列
    q_result = Manager().Queue()  # 结果队列
    for index, param in enumerate(params):
        # param['func']优先级最高
        # 存在    param['func']
        if 'func' in param.keys() and param['func'] != None:
            pass
        # 不存在   param['func']
        else:
            # 有func
            if func != None:
                param['func'] = func
            # 无func
            else:
                msg = 'No func to execute'
                raise exception.ParamException(msg)
        q_param.put(
            {
                'index': index,
                'param': param,
                'skip_exception': skip_exception
            }
        )
    # 单进程运行
    if p_num <= 1:
        _pool_worker(q_param, q_result)
    # 多进程运行
    else:
        processes = []
        for i in range(p_num):
            p = Process(target=_pool_worker, kwargs={'q_param': q_param, 'q_result': q_result})
            processes.append(p)
            p.start()

        def wait_processes(processes):
            for p in processes:
                if p.is_alive():
                    return False
            return True

        # 等待进程均运行完成
        while True:
            if wait_processes(processes):
                break
            else:
                time.sleep(0.15)
    # 整理结果
    for i in range(q_result.qsize()):
        result = q_result.get(block=False, timeout=0)
        index = result['index']
        data = result['data']
        # 按照索引赋值，如果某个参数执行异常并且skip_exception，这个结果为None
        results[index] = data
    return results
