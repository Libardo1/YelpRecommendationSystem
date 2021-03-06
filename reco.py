__author__ = 'Aravindan, Praphull, Vaibhav'

import json
import gc
from scipy import linalg as LAS
import numpy as np
from numpy import linalg as LA
import csv
import scipy.io

def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def low_rank_approx(u, s, v, r):
    Ar = np.zeros((len(u), len(v)))
    for i in xrange(r):
        Ar += s[i] * np.outer(u.T[i], v[i])
    return Ar


'''
jsonarr_users = open("Dataset/yelp_academic_dataset_user.json").readlines()
jsonarr_reviews = open("Dataset/yelp_academic_dataset_review.json").readlines()
jsonarr_business = open("Dataset/yelp_academic_dataset_business.json").readlines()
'''
'''
jsonarr_users = open("Dataset/user_temp.json").readlines()
jsonarr_reviews = open("Dataset/review_temp.json").readlines()
jsonarr_business = open("Dataset/business_temp.json").readlines()
'''

users = []
businesses = []

for jsonstr in open("Dataset/yelp_academic_dataset_user.json").readlines():
    if(jsonstr != ""):
        jsonobj = json.loads(jsonstr)
        users.append(jsonobj["user_id"])

users = unique_list(users)

for jsonstr in open("Dataset/yelp_academic_dataset_business.json").readlines():
    if(jsonstr != ""):
        jsonobj = json.loads(jsonstr)
        businesses.append(jsonobj["business_id"])

businesses = unique_list(businesses)


print "Test Before Matrix Creation"

rating_matrix = np.zeros((len(users),len(businesses)), dtype=int)

for jsonstr in open("Dataset/yelp_academic_dataset_review.json").readlines():
    if(jsonstr != ""):
        jsonobj = json.loads(jsonstr)
        rating_matrix[users.index(jsonobj["user_id"])][businesses.index(jsonobj["business_id"])] = jsonobj["stars"]

print "Test After Matrix Creation"

#scipy.io.savemat('rating_matrix.mat', mdict={'rating_matrix': rating_matrix})

(m,n) = rating_matrix.shape
ratingDict = {}
W = np.zeros((m, n), dtype=int)
for j in xrange(m):
    W[j] = [1 if z > 0 else 0 for z in rating_matrix[j]]
    sum = W[j].sum()
    if sum in ratingDict:
        ratingDict[sum] = ratingDict[sum] + 1
    else:
        ratingDict[sum] = 1

print "Weight Mtrix Creation Successful"

for j in xrange(1,100):
    if j in ratingDict:
        print "Users with", j, " ratings = ", ratingDict[j]
