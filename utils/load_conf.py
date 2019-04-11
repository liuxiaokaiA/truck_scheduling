import logging
import configparser


log = logging.getLogger('default')


def read_fuc(conf_path):
    conf = configparser.ConfigParser()
    try:
        conf.read(conf_path+'default.conf')
    except IOError:
        log.log_mgr.error('file: default.conf can not open')
        return 0
    default_conf = {
        # 'colony_size': conf.getint('ga', 'colony_size'),
    }
    return default_conf


if __name__ == '__main__':
    print read_fuc('conf/')
