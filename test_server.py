from concurrent import futures
import logging
import threading

import grpc
from grpc_reflection.v1alpha import reflection
from api import algorithm_pb2, algorithm_pb2_grpc
from manager.spark_manager import *


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



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    algorithm_pb2_grpc.add_AlgorithmServicer_to_server(Algorithm(), server)
    # the reflection service will be aware of "Greeter" and "ServerReflection" services.
    SERVICE_NAMES = (
        algorithm_pb2.DESCRIPTOR.services_by_name['Algorithm'].full_name,
       reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50057')
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