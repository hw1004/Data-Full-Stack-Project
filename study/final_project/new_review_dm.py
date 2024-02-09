from datetime import date, datetime
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql import *
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt #그래프 패키지 모듈 등록
import pymysql
import findspark
from hdfs import InsecureClient
import csv

def create_conf():
    conf_dw = {
        'url':'jdbc:mysql://localhost:3306/final_project?characterEncoding=utf8&serverTimezone=Asia/Seoul'
        ,'props':{
        'user':'bigMysql',
        'password':'bigMysql1234@'   
        }
    }
    conf_dm = {
        'url':'jdbc:mysql://localhost:3306/final_project_DM?characterEncoding=utf8&serverTimezone=Asia/Seoul'
        ,'props':{
        'user':'bigDM',
        'password':'bigDM1234@'   
        }
    }
    return [conf_dw, conf_dm]

def get_spark_session():
    findspark.init()
    return SparkSession.builder.getOrCreate()

def get_data(config, table_name):
    spark_sc = get_spark_session()
    tmp = spark_sc.read.jdbc(url=config['url'], table=table_name, properties=config['props'])
    return tmp

def add_review_id(data):
    data = data.withColumn('new_review_id', monotonically_increasing_id())
    return data

def save_data(config, df, table_name):
    return df.write.jdbc(url=config['url'], table=table_name , mode='overwrite', properties=config['props'])



if __name__ == '__main__':
    conf = create_conf()
    data = get_data(conf[0], 'new_review')
    data = add_review_id(data)
    save_data(conf[1], data, 'new_review')