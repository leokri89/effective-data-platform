
import sys
sys.path.insert(0,'/mnt/efs/site-package')

import json, pickle

import numpy, pandas, xgboost

def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': output
    }
