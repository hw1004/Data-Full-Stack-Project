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

JDBC = {
      'url':'jdbc:mysql://localhost:3306/final_project?characterEncoding=utf8&serverTimezone=Asia/Seoul'
     ,'props':{
      'user':'bigMysql',
      'password':'bigMysql1234@'   
      }
}

def get_spark_session():
    findspark.init()
    return SparkSession.builder.getOrCreate()

def get_data(path):
    file_name = 'hdfs://localhost:9000/final/' + path
    spark_sc = get_spark_session()
    tmp = spark_sc.read.csv(file_name, header=True, encoding='utf-8')
    tmp.printSchema()
    return tmp

def dw_save(save_data):
    save_data.write.jdbc(url=JDBC['url'], table='new_review', mode='overwrite', properties=JDBC['props'])

if __name__ == '__main__':
    data = get_data('new_review.csv')
    dw_save(data)