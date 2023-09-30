#!/usr/bin/env python3
import pandas
import argparse
import logging
import sys
from utils.cleaner import clean_df
from utils.normalizer import normalize_df
from utils.animator import play


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
args = parser.parse_args()


df = pandas.read_excel(args.input_file)
logger.info('Read excel file %s.', args.input_file)

cleaned_df = clean_df(df)
logger.info('Cleaned dataframe.')

normalized_data = normalize_df(cleaned_df, delta=0.1)
logger.info('Normalized data.')

logger.info('Loading animation...')
play(normalized_data, frames_per_second=float(args.fps))

logger.info('DONE')
