'''
Author: Shawshank980924 Akatsuki980924@163.com
Date: 2022-06-09 10:55:57
LastEditors: Shawshank980924 Akatsuki980924@163.com
LastEditTime: 2022-06-13 19:01:06
FilePath: /sxx/grpc_demo/grpc_server/datapipe/replay.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%A
'''
import functools
from pyspark.sql import SparkSession
import datetime
from kafka import KafkaProducer,KafkaAdminClient
from kafka.admin import NewTopic
import time
def DataReplay(begin_date,end_date,topic_name):
    adminKafka = KafkaAdminClient(bootstrap_servers=['hpc01:9092','hpc02:9092','hpc03:9092','hpc04:9092','hpc05:9092','hpc06:9092','hpc07:9092','hpc08:9092','hpc09:9092','hpc10:9092'],api_version=(2,6,0))
    if topic_name in adminKafka.list_topics():
        dl = []
        dl.append(topic_name)
        adminKafka.delete_topics(dl)
        time.sleep(10)
        # print('===========ok2')
    l = []
    l.append(NewTopic(topic_name,30,3))
    adminKafka.create_topics(l)
    begin_date = datetime.datetime.strptime(begin_date, "%Y_%m_%d")
    end_date = datetime.datetime.strptime(end_date, "%Y_%m_%d")
    delta = datetime.timedelta(days=1)
    while begin_date <= end_date:
        print(begin_date)
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
    # df.show(20)
    spark.read.orc(path).orderBy('timestamp').rdd.foreachPartition(functools.partial(go2kafka,topic=topic))
    # for row in df.collect():
    #     producer.send(topic,bytes(row[0]))
    
def go2kafka(partition,topic):
    p1 = KafkaProducer(acks=1,bootstrap_servers=['hpc01:9092','hpc02:9092','hpc03:9092','hpc04:9092','hpc05:9092','hpc06:9092','hpc07:9092','hpc08:9092','hpc09:9092','hpc10:9092'],api_version=(2,6,0))
    for row in partition:
        p1.send(topic,bytes(row[1]))
    p1.close()
    return 0
        

# DataReplay('2017_10_17','2017_10_17','trans_Demo')

# orc2kafka('/sxx/archive/2017/07/01.orc','replaydemo_2017_07_01')
# DataReplay('2017_01_01','2017_02_01')
# spark= SparkSession.builder \
#     .appName('dataReplay') \
#     .master('local') \
#     .getOrCreate()
# l1 = "/sxx/archive/2017/07/01.orc"
# l2 = '/sxx/archive/2017/07/02.orc'
# t1=datetime.datetime.now()
# df = spark.read.orc(l)
# t2=datetime.datetime.now()
# # print('total')
# # print(df.show())
# count = df.count()
# # t2=datetime.datetime.now()
# print(count)  
# print((t2-t1).total_seconds())
admin = KafkaAdminClient(bootstrap_servers=['hpc01:9092','hpc02:9092','hpc03:9092','hpc04:9092','hpc05:9092','hpc06:9092','hpc07:9092','hpc08:9092','hpc09:9092','hpc10:9092'],api_version=(2,6,0))
print(admin.delete_topics(admin.list_topics()))

