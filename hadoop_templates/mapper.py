#!/bin/python
#coding=utf-8

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input):
    for line in input:
        vec = line.strip().split('\t')
        if len(vec) < 7:
            continue
        timestamp = vec[1]
        
        house = json.loads(vec[6])
        
        if 'user_id' in house and 'city_id' in house and 'detail_id_type' in house and house['user_id'] != None and house['city_id'] == 110000 and house['detail_id_type'] == 1:
#        if house['city_id'] == 110000 and house['detail_id_type'] == 1:
            output_str = '{user_id}\t{timestamp}\t{house_pkid}'.format(
                          user_id = house['user_id'],
                          timestamp = timestamp,
                          house_pkid = house['detail_id'])
            print output_str

if __name__ == '__main__':
    run(sys.stdin)
