from doctest import FAIL_FAST
from enum import Enum
from re import A

# 加密方式
# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad
# key = b'hzqhzq11'
# BLOCK_SIZE = 32
# des = DES.new(key,DES.MODE_ECB)
# encrypted_path = des.encrypt(pad(hdfs_path.encode("utf-8"), BLOCK_SIZE))
# plain_path = unpad(des.decrypt(encrypted_path), BLOCK_SIZE).decode()

# 时间单位
class UnitEnum(Enum):
    mouth = 2592000
    day = 86400
    hour = 3600
    minute = 60
    second = 1

# yarn rest api的IP和Port
yarn_ip='hpc04'
yarn_port='8088'

# spark 提交命令模板, 使用队列algorithm
# TODO: need add --queue algorithm \
spark_submit_cmd_template = \
'spark-submit --master yarn \
--deploy-mode cluster \
--driver-memory {driver_memory}g \
--driver-cores {driver_cores} \
--executor-memory {executor_memory}g \
--executor-cores {executor_cores} \
--num-executors {num_executors} \
--class {class_name} \
{args} \
{jar_path}'

# 从spark_algorithm_begin_id开始的algorithm_id都是用spark实现的
spark_algorithm_begin_id = 10

# algorithm_id与algorithm对应表(enum Name->id)
class AlgorithmID(Enum):
    Sampling = 0
    NebulaQuery = 1
    EdgeQuery = 2
    VertexQuery = 3
    VertAttrQuery = 4
    EdgeAttrQuery = 5
    MatchTriangle = 6
    MatchQuadrilateral = 7
    ShortestPath = 10
    ConnectedComponent = 13
    StronglyConnectedComponent = 14
    GlobalClusteringCoefficient = 15
    LocalClusteringCoefficient = 16
    AvgClusteringCoefficient = 17
    BFS = 18
    DegreeCentrality = 19
    Closeness = 20
    BetweennessCentrality = 21
    PageRank = 22
    LabelPropagation = 23
    TriangleCount = 24

# algorithm_id与algorithm的class的名字对应表(tuple: algorithm_id为index)
algorithm_class_name = \
('Sampling',                        'NebulaQuery',              'EdgeQuery',                    'VertexQuery',                  # 0  1  2  3 
 'VertAttrQuery',                   'EdgeAttrQuery',            'MatchTriangle',                'MatchQuadrilateral',           # 4  5  6  7 
 '',                                '',                         'ShortestPath',                 '',                             # 8  9  10 11
 '',                                'ConnectedComponent',       'StronglyConnectedComponent',   'GlobalClusteringCoefficient',  # 12 13 14 15
 'LocalClusteringCoefficient',      'AvgClusteringCoefficient', 'BFS',                          'DegreeCentrality',             # 16 17 18 19
 'Closeness',                       'BetweennessCentrality',    'PageRank',                     'LabelPropagation',             # 20 21 22 23
 'TriangleCount',                    '',                        '',                             '')                             # 24 25 26 27

# algorithm_id与algorithm的jar包地址对应表(tuple: algorithm_id为index)
algorithm_jar_path = (
    '', # 0
    '', # 1
    '', # 2
    '', # 3
    '', # 4
    '', # 5
    '', # 6
    '', # 7
    '', # 8
    '', # 9
    '../algorithm/ShortestPath.jar', # 10
    '', # 11
    '', # 12
    '../algorithm/ConnectedComponent.jar', # 13
    '../algorithm/StronglyConnectedComponent.jar', # 14
    '../algorithm/GlobalClusteringCoefficient.jar', # 15
    '../algorithm/LocalClusteringCoefficient.jar', # 16
    '../algorithm/AvgClusteringCoefficient.jar', # 17
    '../algorithm/BFS.jar', # 18
    '../algorithm/DegreeCentrality.jar', # 19
    '../algorithm/Closeness.jar', # 20
    '', # 21
    '../algorithm/PageRank.jar', # 22
    '../algorithm/LabelPropagation.jar', # 23
    '../algorithm/TriangleCount.jar', # 24
    '', # 25
    '', # 26
    '', # 27
)

# 每个缓存的时间戳，还没有缓存的id对应值为None
algorithm_cache_time_none=[None] * 28
algorithm_cache_time=dict()
# 每个算法是否需要缓存，不存在的算法id置为None
algorithm_need_cache= \
(False, False,  False,  False,  # 0  1  2  3 
 False, False,  True,   True,   # 4  5  6  7 
 None,  None,   False,  None,   # 8  9  10 11
 None,  False,  False,  True,   # 12 13 14 15
 True,  True,   False,  False,  # 16 17 18 19
 True,  False,  False,  False,  # 20 21 22 23
 True,  None,   None,   None)   # 24 25 26 27

# 算法缓存的hdfs基地址
algorithm_base_output_path='/algorithm'

# 内存消耗大的算法包
LargeMemoryConsumptions = set([AlgorithmID.GlobalClusteringCoefficient.value,
                               AlgorithmID.LocalClusteringCoefficient.value,
                               AlgorithmID.AvgClusteringCoefficient.value,
                               AlgorithmID.TriangleCount.value,
                               AlgorithmID.ShortestPath.value,
                               AlgorithmID.Closeness.value,
                               AlgorithmID.LabelPropagation.value,
                               AlgorithmID.BFS.value])