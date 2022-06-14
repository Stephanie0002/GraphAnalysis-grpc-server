'''
Author: Shawshank980924 Akatsuki980924@163.com
Date: 2022-06-13 15:26:25
LastEditors: Shawshank980924 Akatsuki980924@163.com
LastEditTime: 2022-06-13 18:31:22
FilePath: /sxx/grpc_demo/grpc_server/client.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%A
'''

from api import algorithm_pb2,algorithm_pb2_grpc
import grpc
channel = grpc.insecure_channel('hpc01:50056')
stub = algorithm_pb2_grpc.DataPipeStub(channel)
print(stub.Replay(algorithm_pb2.ReplayRequest(dataset_name='trans',topic_name='trans_replay',start_timestamp=1602880445,end_timestamp=1602903412)))