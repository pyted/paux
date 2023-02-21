import logging
import os
import time
import traceback
import paux.date as _date


class Log():
    LOG_DIRPATH: str  # './LOG_DATA' 日志文件夹
    FILE_LEVEL: str  # 'INFO' 文件输出级别
    CONSOLE_LEVEL: str  # 'INFO' 控制台打印级别
    SPLIT_LEVEL:bool # 不同级别信息分文件存储
    TIMEZONE:str # 时区


    def __init__(
            self,
            log_dirpath='./LOG_DATA',
            timezone = 'Asia/Shanghai',
            file_level='INFO',
            console_level='DEBUG',
            split_level=True,
    ):
        '''
        :param log_dirpath: 日志文件夹
        :param file_level: 文件输出级别
        :param console_level: 控制台打印级别
        :param split_level: 不同级别信息分文件存储
        '''
        self.LOG_DIRPATH = log_dirpath
        self.FILE_LEVEL = file_level
        self.CONSOLE_LEVEL = console_level
        self.SPLIT_LEVEL = split_level
        self.TIMEZONE = timezone

        if not os.path.isdir(self.LOG_DIRPATH):
            os.makedirs(self.LOG_DIRPATH)

    def get_logger(self, level):
        if not os.path.isdir(self.LOG_DIRPATH):
            os.makedirs(self.LOG_DIRPATH)
        if self.TIMEZONE == 'America/New_York':
            date_str = _date.to_fmt(time.time()*1000,timezone=self.TIMEZONE,fmt='%d-%m-%Y')
        else:
            date_str = _date.to_fmt(time.time()*1000,timezone=self.TIMEZONE,fmt='%Y-%m-%d')
        if self.SPLIT_LEVEL:
            log_filename = '{date}_{level}.log'.format(
                date = date_str,
                level = level.upper(),
            )
        else:
            log_filename = '{date}.log'.format(
                date = date_str,
            )
        log_filepath = os.path.join(self.LOG_DIRPATH, log_filename)
        file_handler = logging.FileHandler(log_filepath)  # 输出到文件
        console_handler = logging.StreamHandler()  # 输出到控制台
        file_handler.setLevel(self.FILE_LEVEL)  # FILE_LEVEL以上才输出到文件
        console_handler.setLevel(self.CONSOLE_LEVEL)  # CONSOLE_LEVEL以上才输出到控制台
        if traceback.format_exc().strip() != 'NoneType: None':
            fmt = '%(asctime)s [%(levelname)s] {message}\ntraceback:{traceback}'.format(filepath=__file__, message='%(message)s', traceback=str(traceback.format_exc()))
        else:
            fmt = '%(asctime)s [%(levelname)s] {message}'.format(filepath=__file__, message='%(message)s')
        formatter = logging.Formatter(fmt)
        file_handler.setFormatter(formatter)  # 设置文件内容格式
        console_handler.setFormatter(formatter)  # 设置控制台内容格式
        logger = logging.getLogger('updateSecurity')
        logger.setLevel(level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger, [file_handler, console_handler]

    def debug(self, msg):
        LEVEL = 'DEBUG'
        logger, handlers = self.get_logger(level=LEVEL)
        logger.debug(msg)
        for handler in handlers:
            logger.removeHandler(handler)

    def info(self, msg):
        LEVEL = 'INFO'
        logger, handlers = self.get_logger(level=LEVEL)
        logger.info(msg)
        for handler in handlers:
            logger.removeHandler(handler)

    def error(self, msg):
        LEVEL = 'ERROR'
        logger, handlers = self.get_logger(level=LEVEL)
        logger.error(msg)
        for handler in handlers:
            logger.removeHandler(handler)

    def warn(self, msg):
        LEVEL = 'WARN'
        logger, handlers = self.get_logger(level=LEVEL)
        logger.warning(msg)
        for handler in handlers:
            logger.removeHandler(handler)

    def critical(self, msg):
        LEVEL = 'CRITICAL'
        logger, handlers = self.get_logger(level=LEVEL)
        logger.critical(msg)
        for handler in handlers:
            logger.removeHandler(handler)