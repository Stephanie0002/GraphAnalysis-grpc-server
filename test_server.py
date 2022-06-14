'''
Author: Shawshank980924 Akatsuki980924@163.com
Date: 2022-06-09 08:33:42
LastEditors: Shawshank980924 Akatsuki980924@163.com
LastEditTime: 2022-06-14 14:31:59
FilePath: /sxx/grpc_demo/grpc_server/test_server.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from concurrent import futures
from ensurepip import bootstrap
import logging
import threading
from unittest import result

import grpc
from grpc_reflection.v1alpha import reflection
from api import algorithm_pb2, algorithm_pb2_grpc
from datapipe.replay import orc2kafka
from manager.spark_manager import *

from datapipe.replay import DataReplay
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from hdfs.client import Client
import datetime


class Algorithm(algorithm_pb2_grpc.AlgorithmServicer):
    def _GetSparkReply(self, app_id, hdfs_path):
        if app_id is None: # get exceptions
            error_messsage = hdfs_path
            return algorithm_pb2.AlgorithmReply(
                state='failed', 
                timestamp=None,
                app_id=None,
                hdfs_path=None,
                message='算法执行失败! 错误信息是：' + error_messsage
            )
        elif app_id == 'cached': # return Cached result in hdfs
            return algorithm_pb2.AlgorithmReply(
                state='cached', 
                timestamp=int(hdfs_path.rsplit('_',1)[1]),
                app_id=None,
                hdfs_path=hdfs_path,
                message='算法已有缓存! 时间戳是: ' + hdfs_path.split('_')[-1]
            )
        elif app_id == 'spark failed': # spark failed before get app id
            return algorithm_pb2.AlgorithmReply(
                state='failed', 
                timestamp=int(hdfs_path.rsplit('_',1)[1]),
                app_id=None,
                hdfs_path=hdfs_path,
                message='算法执行失败! spark在accept前失败!'
            )
        else: # executing, wait for result
            print(app_id, hdfs_path)
            return algorithm_pb2.AlgorithmReply(
                state='started', 
                timestamp=int(hdfs_path.rsplit('_',1)[1]),
                app_id=app_id,
                hdfs_path=hdfs_path,
                message='算法开始运行! spark应用id是: ' + app_id
            )
    
    def ExecuteAlgorithm(self, request, context):
        timeArray = time.localtime(time.time())
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print(timeStr+":: Get Request: ", request.algorithm_id, request.kwargs)
        if request.algorithm_id >= spark_algorithm_begin_id:
            app_id, hdfs_path=SparkManager.executeSpark(request.algorithm_id, request.use_cache, request.kwargs)
            reply = self._GetSparkReply(app_id, hdfs_path)            
        else:
            #TODO: nebula manager
            pass
        return reply

    def SparkQueryState(self, request, context):
        timeArray = time.localtime(time.time())
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        app_id = request.app_id
        state, finalStatus = SparkManager.queryState(app_id=app_id)
        print(timeStr+":: Get Request: ", app_id, state, finalStatus)
        return algorithm_pb2.SparkQueryReply(state=state, finalStatus=finalStatus)
    
class DataPipe(algorithm_pb2_grpc.DataPipeServicer):
    def __init__(self):
        self.client = Client('http://192.168.1.13:9009')
        self.producer = KafkaProducer(acks=1,bootstrap_servers=['hpc01:9092','hpc02:9092','hpc03:9092','hpc04:9092','hpc05:9092','hpc06:9092','hpc07:9092','hpc08:9092','hpc09:9092','hpc10:9092'],api_version=(2,6,0))
    def Replay(self,request,context):
        topic_name = request.topic_name
        timeStArr = time.localtime(request.start_timestamp)
        timeEdArr = time.localtime(request.end_timestamp)
        begin_date = time.strftime("%Y_%m_%d", timeStArr)
        end_date = time.strftime("%Y_%m_%d", timeEdArr)
        st = datetime.datetime.strptime(begin_date,"%Y_%m_%d")
        ed = datetime.datetime.strptime(end_date,"%Y_%m_%d")
        delta = datetime.timedelta(days=1)
        while st <= ed:
            y,m,d = st.strftime("%Y_%m_%d").split('_')
            path = '/sxx/archive/{}/{}/{}.orc'.format(y,m,d)
            if self.client.status(path,strict=False)==None:
                # context.set_details('path: {} does not exist on hdfs'.format(path))
                # context.set_code(grpc.StatusCode.NOT_FOUND)
                # raise context
                return algorithm_pb2.ReplayReply(result='FAIL',error_info='data in {} does not exist!'.format(st.strftime("%Y_%m_%d")))
            st += delta
        # print('===========ok1')
        
        # print('===========ok3')
        threading.Thread(target=DataReplay,args=(begin_date,end_date,topic_name,)).start()
        # print('===========ok4')
        return algorithm_pb2.ReplayReply(result = 'SUCCESS')
            
        
        




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    algorithm_pb2_grpc.add_AlgorithmServicer_to_server(Algorithm(), server)
    algorithm_pb2_grpc.add_DataPipeServicer_to_server(DataPipe(),server)
    # the reflection service will be aware of "Greeter" and "ServerReflection" services.
    SERVICE_NAMES = (
        algorithm_pb2.DESCRIPTOR.services_by_name['Algorithm'].full_name,
       reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50056')
    # 读入现有缓存的状态
    SparkManager.refreshCacheState(False)
    # 持续更新缓存状态 
    t1 = threading.Thread(target=SparkManager.refreshCacheState, args=(True,))
    t1.start()
    server.start()
    print("Wait for request...")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()