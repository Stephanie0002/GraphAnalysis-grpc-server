import logging
import json
import os
import re
import time
import pymysql
from urllib import request, error
from manager.spark_manager_config import *
from manager import spark_manager_config


class SparkManager(object):
    def __init__(self) -> None:
        pass

    # 根据算法id判断是否使用缓存，并给出结果文件将存在hdfs中的路径
    def _getHDFSAddress(algorithm_id: int, graph_space, use_cache:bool) -> str:
        if graph_space not in spark_manager_config.algorithm_cache_time:
            # 若还没有该图空间的缓存维护，初始化algorithm_cache_time[graph_space]
            spark_manager_config.algorithm_cache_time[graph_space]=spark_manager_config.algorithm_cache_time_none
        timestamp = int(time.time())
        cached = False
        if not use_cache:
            output_path=os.path.join(
                algorithm_base_output_path,
                graph_space,
                str(algorithm_id)+'_'+algorithm_class_name[algorithm_id] +'_'+str(timestamp)
            )
            return cached, output_path
        #  有缓存且已有缓存不超过一天未失效则返回缓存
        if algorithm_need_cache[algorithm_id] and \
            spark_manager_config.algorithm_cache_time[graph_space][algorithm_id] is not None and \
            (timestamp - spark_manager_config.algorithm_cache_time[graph_space][algorithm_id])<UnitEnum.day.value:
                cached=True
                cache_path=os.path.join(
                    algorithm_base_output_path,
                    graph_space,
                    str(algorithm_id)+'_'+algorithm_class_name[algorithm_id]+'_'+
                    str(spark_manager_config.algorithm_cache_time[graph_space][algorithm_id])
                )  # e.g: 'hdfs:///algorithm/graph_space/10_ShortestPath_trade_68895230'
                # 直接返回缓存地址
                return cached, cache_path
        #  否则执行spark包并将结果存入文件kwargs['output_path']
        output_path=os.path.join(
            algorithm_base_output_path,
            graph_space,
            str(algorithm_id)+'_'+algorithm_class_name[algorithm_id]+'_'+str(timestamp)
        )  # e.g: 'hdfs:///algorithm/graph_space/10_ShortestPath_68895230'
        return cached, output_path

    def _getSchema(space:str):
        # 300000条数据每个分区
        # connect
        connect = pymysql.connect(host='114.55.66.96',   # 本地数据库
                          port=3306,
                          user='temporal',
                          password='starry@2022',
                          db='temporal_graph',
                          charset='utf8') #服务器名,账户,密码，数据库名称
        cur = connect.cursor()
        # query schema
        try:
            query = "select * from meta where space_name=\"{}\"".format(space)
            cur.execute(query)
        except Exception as e:
            print("查询数据失败:", e)
        else:
            resTuple=cur.fetchone()
            logging.info("[INFO]    查询数据成功，{}-----------------"+str(resTuple))
        # release connection
        cur.close()
        connect.close()
        vertexNum=resTuple[2]
        edgeNum = resTuple[3]
        return (vertexNum, edgeNum)


    # 借助yarn rest API获取spark程序状态
    def queryState(app_id)->str:
        url='http://{ip}:{port}/ws/v1/cluster/apps/{app_id}'\
            .format(ip=yarn_ip, port=yarn_port,app_id=app_id)
        try:
            res = request.urlopen(url)
            if res.status!=200:  # url get失败
                return None, 'HTTPStatus: {}  Query Failed!!!'.format(res.status)
        except error.HTTPError as e:
            print(e)
            return None, 'HTTPStatus: {}  Query Failed!!!'.format(e.code)   
        except Exception as e:
            print(e)
            return None, 'Query Failed!!! {}'.format(str(e))
        else:
            text=res.read().decode()
            dict = json.loads(text)
            # 无终结状态表明程序尚未结束
            if dict['app'].get('finalStatus') is None:
                return dict['app']['state'], 'UnFinished'
            return dict['app']['state'], dict['app']['finalStatus']

    # 读取hdfs文件目录，每分钟更新一次缓存时间戳
    def refreshCacheState(always:bool):
        while(True):
            import sh            
            # 先遍历图空间目录
            dictlist = [ line.rsplit(None,1)[-1] for line in sh.hdfs('dfs','-ls',algorithm_base_output_path).split('\n') if len(line.rsplit(None,1))][1:]
            for dict in dictlist:
                # 先定义空algorithm_cache_time_new
                algorithm_cache_time_new=spark_manager_config.algorithm_cache_time_none.copy()
                # 图空间
                graph_space = dict.rsplit('/', 1)[-1]

                # 若还没有该图空间的缓存维护，初始化algorithm_cache_time[graph_space]
                if graph_space not in spark_manager_config.algorithm_cache_time:
                    spark_manager_config.algorithm_cache_time[graph_space]=spark_manager_config.algorithm_cache_time_none
                
                # 为每个图空间缓存做更新
                filelist = [ line.rsplit(None,1)[-1] for line in sh.hdfs('dfs','-ls',dict).split('\n') if len(line.rsplit(None,1))][1:]
                for file in filelist:
                    ss=file.split('_')
                    index = int(ss[-3].rsplit('/', 1)[-1])
                    timestamp = int(ss[-1])
                    # 保证最新
                    if spark_manager_config.algorithm_cache_time[graph_space][index] is None or \
                       timestamp>=spark_manager_config.algorithm_cache_time[graph_space][index]:
                        algorithm_cache_time_new[index] = timestamp
                    else: # 删除比最新缓存早1天以上的结果
                        if spark_manager_config.algorithm_cache_time[graph_space][index] - timestamp >= UnitEnum.day.value:
                            sh.hdfs('dfs', '-rm', '-r', file)
                # 更新algorithm_cache_time
                spark_manager_config.algorithm_cache_time[graph_space] = algorithm_cache_time_new.copy()
            logging.info("[INFO]    refreshCacheState:-----------------") # +str(spark_manager_config.algorithm_cache_time))
            if not always:
                break
            time.sleep(60)

    # 执行小数据集的算法包
    def _getSparKARG_SmallDataSet(algorithm_id: int, edges:int, kwargs)->str:
        # str(schema[1]//300000) if schema[1]>30000000 else 
        kwargs['partition']='200'
        cores = 8
        memory= 16 if edges<300000 else 32
        return {"cores":cores, "memory":memory}

    # 执行大数据集的算法包
    def _getSparKARG_BigDataSet(algorithm_id: int, edges:int ,kwargs)->str:
        kwargs['partition']=str(edges//300000)
        kwargs['driver.extraJavaOptions']="-XX:PermSize=128M -XX:MaxPermSize=256M"  # 增大栈大小，防止堆栈溢出
        kwargs['dynamicAllocation.enabled']='false' # 禁用动态分配，避免长期不用excutor挂掉
        kwargs['network.timeout']='3600' # 增大网络延时，避免计算耗时长导致excutor挂掉

        cores = 4 if algorithm_id in LargeMemoryConsumptions else 8
        memory= 152
        return {"cores":cores, "memory":memory}

    # 执行大数据集部分数据的算法包
    def _getSparKARG_PartDataSet(algorithm_id: int, vertex:int ,kwargs):
        kwargs['partition']=str(vertex//300000)
        kwargs['dynamicAllocation.enabled']='false' # 禁用动态分配，避免长期不用excutor挂掉
        kwargs['network.timeout']='3600' # 增大网络延时，避免计算耗时长导致excutor挂掉
        cores = 8
        memory= 84
        return {"cores":cores, "memory":memory}

    # 执行spark算法，获得结果地址
    def executeSpark(algorithm_id: int, use_cache:bool, kwargs):
        try:
            # ------------------确认结果文件地址---------------------------
            cached, hdfs_path = SparkManager._getHDFSAddress(algorithm_id, kwargs['graph.space'], use_cache)
            if(cached):# 直接返回缓存地址，不执行spark分析
                return 'cached', hdfs_path
            else:
                kwargs['hdfs_path'] = hdfs_path
            # -----------------填充spark-submit命令-----------------------
            spark_args = ''
            kwargs["withTimeStamp"]=str("timestamp_from" in kwargs)
            schema = SparkManager._getSchema(kwargs['graph.space'])
            if schema[1]<3000000: # 小数据集
                spark_submit_args = SparkManager._getSparKARG_SmallDataSet(algorithm_id, schema[1], kwargs)
            elif "timestamp_from" in kwargs: # 大数据集的部分
                spark_submit_args = SparkManager._getSparKARG_PartDataSet(algorithm_id, schema[0], kwargs)
            else:                  # 全量大数据集
                spark_submit_args = SparkManager._getSparKARG_BigDataSet(algorithm_id, schema[1], kwargs)
                # spark_args+='--queue bigdataset '

            for key in kwargs:
                spark_args+='--conf spark.'+key+'=\''+kwargs[key]+'\' '
            # print(spark_args)
            assert algorithm_class_name[algorithm_id] != '', 'algorithm id doesn\'t exist!!!'
            assert algorithm_id<len(algorithm_class_name) and algorithm_id >= 0, 'algorithm id doesn\'t exist!!!'
            spark_submit_cmd = spark_submit_cmd_template.format(
                driver_memory=spark_submit_args["memory"], driver_cores=spark_submit_args["cores"], 
                executor_memory=spark_submit_args["memory"], executor_cores=spark_submit_args["cores"], num_executors=9, 
                class_name=algorithm_class_name[algorithm_id], args=spark_args, jar_path=algorithm_jar_path[algorithm_id])
            # print(spark_submit_cmd)
            logging.info('[INFO]    spark_submit_cmd: '+spark_submit_cmd)
            
            # ----------------执行spark-submit命令------------------------
            output_file = os.popen(spark_submit_cmd+" 2>&1", 'r')
            find=None
            line = output_file.readline()
            while line:
                find = re.search(r'.*Application report for (application_\d*_\d*).*',line)
                # print('line:'+line)
                if find is not None:
                    app_id = find.group(1)
                    logging.info(app_id)
                    break
                line = output_file.readline()
                # logging.info(line)
            if find is None:
                app_id="spark failed"
            logging.info('get app_id : {} !!!'.format(app_id))
            # print('get app_id : {} !!!'.format(app_id))
            # ---------------返回结果地址---------------------------------
            # print(app_id, hdfs_path)
            return str(app_id), hdfs_path
        except Exception as e:
            print(e)
            return None, str(e)
