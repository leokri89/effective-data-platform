
import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

logging.info('Downloading dados.')
logging.warning('warning')
logging.error('error')
