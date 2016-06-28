#!/bin/python

import sys
import heapq

SIMILAR_USER_NUMBER = 50

class SimilarUser(object):
    def __init__(self, userid, similar_score):
        self.userid = userid
        self.similar_score = similar_score

    def __cmp__(self, other):
        return cmp(self.similar_score, other.similar_score)

    def __str__(self):
        return ':'.join([self.userid, str(self.similar_score)])

def run(input):
    last_user = ""
    similar_user_list = [ ]

    for line in input:
        vec = line.strip().split('\t')
        userid = vec[0]
        
        similar_user_id = vec[1]
        similar_score = float(vec[2])
        similar_user = SimilarUser(similar_user_id, similar_score)

        if last_user == "":
            last_user = userid
            heapq.heappush(similar_user_list, similar_user)
        elif last_user == userid:
            if len(similar_user_list) < SIMILAR_USER_NUMBER:
                heapq.heappush(similar_user_list, similar_user)
            else:
                farthest_user = similar_user_list[0]
                if farthest_user < similar_user:
                    heapq.heappushpop(similar_user_list, similar_user)
        else:

            similar_user_list.sort(reverse=True)
            output_str = '{userid}\t{similar_user_list}'.format(
                         userid = userid,
                         similar_user_list=','.join([str(user) for user in similar_user_list]) )
            print output_str

            last_user = userid
            similar_user_list = []
            heapq.heappush(similar_user_list, similar_user)

    similar_user_list.sort(reverse=True)
    output_str = '{userid}\t{similar_user_list}'.format(
                 userid = userid,
                 similar_user_list=','.join([str(user) for user in similar_user_list]) )
    print output_str

if __name__ == '__main__':
    run(sys.stdin)
