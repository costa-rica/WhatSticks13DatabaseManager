import os
from ws_config import ConfigWorkstation, ConfigDev, ConfigProd
import logging
from logging.handlers import RotatingFileHandler

match os.environ.get('WS_CONFIG_TYPE'):
    case 'dev':
        config = ConfigDev()
        print('- WhatSticks13DatabaseManager/config: Development')
    case 'prod':
        config = ConfigProd()
        print('- WhatSticks13DatabaseManager/config: Production')
    case _:
        config = ConfigWorkstation()
        print('- WhatSticks13DatabaseManager/config: Local')



#Setting up Logger
app_name = "WS11DatabaseManager"
# formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter = logging.Formatter(f'%(asctime)s - {app_name} - %(name)s - [%(filename)s:%(lineno)d] - %(message)s')

#initialize a logger
logger_db_manager = logging.getLogger(__name__)
logger_db_manager.setLevel(logging.DEBUG)

if not os.path.exists(config.PROJECT_RESOURCES):
    os.makedirs(config.PROJECT_RESOURCES)

#where do we store logging information
file_handler = RotatingFileHandler(os.path.join(config.PROJECT_RESOURCES,'database_manger.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

#where the stream_handler will print
stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter_terminal)
stream_handler.setFormatter(formatter)

logger_db_manager.addHandler(file_handler)
logger_db_manager.addHandler(stream_handler)
