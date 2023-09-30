#!/usr/bin/env python3
import pandas
import argparse
import logging
import sys
from utils.cleaner import clean_df
from utils.normalizer import normalize_df
from utils.animator import play
from utils.errors import ConfigurationError


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(message)s')
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    return logger


logger = get_logger()
logger.info('Starting Pixel Pirates')

parser = argparse.ArgumentParser(
    prog='Pixel Pirates',
    description='Visualizes object data relative to vehicle.')
parser.add_argument('-i', '--input-file', required=True,
                    dest='input_file')
parser.add_argument('-f', '--fps', required=True,
                    dest='fps')
parser.add_argument('-o', '--objects', required=True,
                    dest='objects')
parser.add_argument('-c', '--object-colors', required=True,
                    dest='object_colors')
args = parser.parse_args()


object_names = args.objects.split(',')
object_colors = [tuple([int(i) for i in c.split(':')])
                 for c in args.object_colors.split(',')]
if len(object_names) != len(object_colors):
    msg = ('Number of object names and colors do not match: '
           f'{len(object_names)} != {len(object_colors)} '
           f'==> len({object_names}) != len({object_colors})')
    raise ConfigurationError(msg)

df = pandas.read_excel(args.input_file)
logger.info('Read excel file %s.', args.input_file)

cleaned_df = clean_df(df, object_names)
logger.info('Cleaned dataframe.')

normalized_data = normalize_df(
    cleaned_df, delta=0.1, object_names=object_names)
logger.info('Normalized data.')

logger.info('Loading animation...')
play(normalized_data,
     frames_per_second=float(args.fps),
     object_names=object_names,
     object_colors=object_colors)

logger.info('DONE')
