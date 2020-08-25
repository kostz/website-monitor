import logging
import sys


def initLogger(module, level=logging.INFO):
    logger = logging.getLogger(module)
    logger.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logo(logger, module)
    return logger


def logo(l, n):
    from pyfiglet import Figlet
    f = Figlet(font='rowancap', width=300)
    l.info('\n\n' + f.renderText(n) + '\n  2018-2020, kost zhukov\n\n')
