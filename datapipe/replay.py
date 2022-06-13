'''
Author: Shawshank980924 Akatsuki980924@163.com
Date: 2022-06-09 10:55:57
LastEditors: Shawshank980924 Akatsuki980924@163.com
LastEditTime: 2022-06-10 22:47:43
FilePath: /sxx/grpc_demo/grpc_server/datapipe/replay.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%A
'''
from pyspark.sql import SparkSession
from hdfs.client import Client
import datetime
from kafka import KafkaProducer,KafkaAdminClient
import time
def DataReplay(begin_date,end_date,topic_name):
    # begin_date = time.localtime(begin_date)
    # end_date = time.localtime(end_date)
    # begin_date = datetime.datetime.strptime(begin_date, "%Y_%m_%d")
    # end_date = datetime.datetime.strptime(end_date, "%Y_%m_%d")
    begin_date = datetime.datetime.strptime(begin_date, "%Y_%m_%d")
    end_date = datetime.datetime.strptime(end_date, "%Y_%m_%d")
    delta = datetime.timedelta(days=1)
    while begin_date <= end_date:
        y,m,d = begin_date.strftime("%Y_%m_%d").split('_')
        path = '/sxx/archive/{}/{}/{}.orc'.format(y,m,d)
        orc2kafka(path,topic_name)
        begin_date+=delta
    
    

def orc2kafka(path,topic):
    producer = KafkaProducer(acks=1,bootstrap_servers=['hpc01:9092','hpc02:9092','hpc03:9092','hpc04:9092','hpc05:9092','hpc06:9092','hpc07:9092','hpc08:9092','hpc09:9092','hpc10:9092'],api_version=(2,6,0))
    spark= SparkSession.builder \
    .appName('dataReplay') \
    .master('local') \
    .getOrCreate()
    df = spark.read.orc(path).orderBy('timestamp').drop('timestamp')
    # df.show(20)
    for row in df.collect():
        producer.send(topic,bytes(row[0]))

# DataReplay('2017','10','01')

# orc2kafka('/sxx/archive/2017/07/01.orc','replaydemo_2017_07_01')
# DataReplay('2017_01_01','2017_02_01')
spark= SparkSession.builder \
    .appName('dataReplay') \
    .master('local') \
    .getOrCreate()
l1 = "/sxx/archive/2017/07/01.orc"
l2 = '/sxx/archive/2017/07/02.orc'
t1=datetime.datetime.now()
df = spark.read.orc(l)
t2=datetime.datetime.now()
# print('total')
# print(df.show())
count = df.count()
# t2=datetime.datetime.now()
print(count)  
print((t2-t1).total_seconds())


