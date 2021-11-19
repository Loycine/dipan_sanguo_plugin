import time
import os



import logging
def init_local_logger(logFilename, loggerName):
    logging.basicConfig(
                    level    = logging.INFO,
                    format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt  = '%Y-%m-%d %H:%M:%S',
                    filename = logFilename,
                    filemode = 'a+')
  
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console.setFormatter(formatter)
    logging.getLogger(loggerName).addHandler(console)
    return logging.getLogger(loggerName)

def main_loop():
    cnt = 1
    while True:
        logger.info(f'loop_times: {cnt}')
        os.system('python verifycode.py')
        os.system('python getReward.py')
        os.system('python sendRes.py')
        # os.system('python schedule.py')

        os.system('python government.py')
        os.system('python market.py')
        os.system('python official.py')
        os.system('python city.py')
        os.system('python technology.py')
        time.sleep(600)
        cnt = cnt + 1


if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    main_loop()