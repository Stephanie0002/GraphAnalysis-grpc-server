from threading import Lock, Thread
from typing import List
from nebula2.Config import Config
from nebula2.common.ttypes import Edge, ErrorCode, Vertex
from nebula2.gclient.net import ConnectionPool
from nebula2.sclient.GraphStorageClient import GraphStorageClient
from nebula2.mclient import MetaCache
from nebula2.data import ResultSet
from nebula2.sclient.ScanResult import EdgeResult, VertexResult
import ray
import ray.util.queue

from funs.reps_fomat_parse import GetResultTable

result_queue = ray.util.queue.Queue()

@ray.remote
class Connects:
    def __init__(self, space:str) -> None:
        self.execute_times=0
        self.space = space
        # 定义配置
        config = Config()
        config.max_connection_pool_size = 2000
        graph_addrs = [('server-1', 9669), ('server-2', 9669), ('server-3', 9669), ('server-4', 9669)] # 
        meta_addrs = [('server-1', 9559), ('server-2', 9559), ('server-3', 9559), ('server-4', 9559)]
        # 初始化连接池
        self.connection_pool = ConnectionPool()
        # 如果给定的服务器正常，则返回 true，否则返回 false。
        ok = self.connection_pool.init(graph_addrs, config)

        #连接graphd
        meta_cache = MetaCache(meta_addrs, 50000)
        self.graph_storage_client = GraphStorageClient(meta_cache)

        print(ok)

    def scan_vertex(self, tag:str) -> List[VertexResult]:
        result = self.graph_storage_client.scan_vertex(space_name=self.space, tag_name=tag)
        answer = []
        while(result.has_next()):
            temp = result.next()
            for item in temp:
                answer.append(item)
        return answer

    def scan_edge(self, edge_type:str) -> List[EdgeResult]:
        result = self.graph_storage_client.scan_edge(space_name=self.space, edge_name=edge_type)
        answer = []
        while(result.has_next()):
            temp = result.next()
            for item in temp:
                answer.append(item)
        return answer

    def exe_statement_direct(self, statement:str) -> ResultSet:
        # 从连接池中获取会话
        with self.connection_pool.session_context('root', 'nebula') as session:
            # 选择图空间
            session.execute('USE {}'.format(self.space)) # ('USE hzq_test') # ('USE tran')
            #执行查询
            result = session.execute(statement)
            #解析结果
            assert result.is_succeeded(), result.error_msg()
            assert '' == result.error_msg()
            assert result.latency() > 0
            assert ErrorCode.SUCCEEDED == result.error_code()
            
            result_list=[]
            if(result.row_size()>0):
                result = GetResultTable(result)
                for i in range(0, len(result)):
                    list = []
                    for j in range(0, len(result[i])-1):
                        list.append(result[i][j])
                    list.sort()
                    temp = tuple(list)
                    if(len(set(temp))==len(result[i])-1):
                        result_list.append(temp)
            #回传结果
            return result_list


    def exe_thread(self, ans_queue, statement:str) -> None:
        # 从连接池中获取会话
        with self.connection_pool.session_context('root', 'nebula') as session:
            # 选择图空间
            session.execute('USE {}'.format(self.space)) # ('USE hzq_test') # ('USE tran')
            #执行查询
            result = session.execute(statement)
            #解析结果
            assert result.is_succeeded(), result.error_msg()
            assert '' == result.error_msg()
            assert result.latency() > 0
            assert ErrorCode.SUCCEEDED == result.error_code()
            
            result_list=[]
            if(result.row_size()>0):
                result = GetResultTable(result)
                for i in range(0, len(result)):
                    list = []
                    for j in range(0, len(result[i])-1):
                        list.append(result[i][j])
                    list.sort()
                    temp = tuple(list)
                    if(len(set(temp))==3):
                        result_list.append(temp)
            #回传结果
            result_id = ray.put(result_list)
            ans_queue.put(result_id)
    
    def exe_statement_parrallel(self, ans_queue, statement:str) -> None:
        self.execute_times+=1
        thread = Thread(target=self.exe_thread, name='execute-thread-{}'.format(self.execute_times), 
                        kwargs={"ans_queue": ans_queue, "statement": statement})
        thread.start()

    def __reduce__(self) -> None:
        # 关闭连接池
        self.connection_pool.close()