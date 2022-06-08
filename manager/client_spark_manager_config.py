from enum import Enum

# 时间单位
class UnitEnum(Enum):
    mouth = 2592000
    day = 86400
    hour = 3600
    minute = 60
    second = 1

# algorithm_id与algorithm对应表(enum Name->id)
class AlgorithmID(Enum):
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
 '',                                '',                         'ShortestPath',                 'ConnectedComponentNum',        # 8  9  10 11
 'StronglyConnectedComponentNum',   'ConnectedComponent',       'StronglyConnectedComponent',   'GlobalClusteringCoefficient',  # 12 13 14 15
 'LocalClusteringCoefficient',      'AvgClusteringCoefficient', 'BFS',                          'DegreeCentrality',             # 16 17 18 19
 'Closeness',                       'BetweennessCentrality',    'PageRank',                     'LabelPropagation',             # 20 21 22 23
 'TriangleCount',                    '',                        '',                             '')                             # 24 25 26 27