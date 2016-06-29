#!/bin/bash

from pyspark import SparkContext
import json

def filter(record):
    vec = record.strip().split('\t')
    if len(vec) < 7:
        return False
    try:
        house = json.loads(vec[6])
    except Exception as e:
        return False

    if 'user_id' in house and 'city_id' in house and 'detail_id_type' in house and house['user_id'] != None and house['city_id'] == 110000 and house['detail_id_type'] == 1:
        return True

    return False

def output(record):
    vec = record.strip().split('\t')
    timestamp = vec[1]
    house = json.loads(vec[6])
    output_str = '{user_id}\t{timestamp}\t{house_pkid}'.format(
                          user_id = house['user_id'],
                          timestamp = timestamp,
                          house_pkid = house['detail_id'])
    return output_str


def main():
    sc = SparkContext()

    input = sc.textFile('INPUT_PATH*')
    rdd = input.filter(filter) \
               .map(output) \
               .sortBy(lambda x: x.split('\t')[0]) \
               .coalesce(2) \
               .saveAsTextFile('OUTPUT_PATH')
#   hdfs://master:port/path
if __name__ == '__main__':
    main()
