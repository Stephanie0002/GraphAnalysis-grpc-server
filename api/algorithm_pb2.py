# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: algorithm.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='algorithm.proto',
  package='algorithm',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x61lgorithm.proto\x12\talgorithm\"\xa3\x01\n\x10\x41lgorithmRequest\x12\x14\n\x0c\x61lgorithm_id\x18\x01 \x01(\x03\x12\x37\n\x06kwargs\x18\x02 \x03(\x0b\x32\'.algorithm.AlgorithmRequest.KwargsEntry\x12\x11\n\tuse_cache\x18\x03 \x01(\x08\x1a-\n\x0bKwargsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"f\n\x0e\x41lgorithmReply\x12\r\n\x05state\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\t\x12\x11\n\thdfs_path\x18\x04 \x01(\t\x12\x0f\n\x07message\x18\x05 \x01(\t\"#\n\x11SparkQueryRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\"5\n\x0fSparkQueryReply\x12\r\n\x05state\x18\x01 \x01(\t\x12\x13\n\x0b\x66inalStatus\x18\x02 \x01(\t2\xa8\x01\n\tAlgorithm\x12L\n\x10\x45xecuteAlgorithm\x12\x1b.algorithm.AlgorithmRequest\x1a\x19.algorithm.AlgorithmReply\"\x00\x12M\n\x0fSparkQueryState\x12\x1c.algorithm.SparkQueryRequest\x1a\x1a.algorithm.SparkQueryReply\"\x00\x62\x06proto3'
)




_ALGORITHMREQUEST_KWARGSENTRY = _descriptor.Descriptor(
  name='KwargsEntry',
  full_name='algorithm.AlgorithmRequest.KwargsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='algorithm.AlgorithmRequest.KwargsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='algorithm.AlgorithmRequest.KwargsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=194,
)

_ALGORITHMREQUEST = _descriptor.Descriptor(
  name='AlgorithmRequest',
  full_name='algorithm.AlgorithmRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='algorithm_id', full_name='algorithm.AlgorithmRequest.algorithm_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kwargs', full_name='algorithm.AlgorithmRequest.kwargs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='use_cache', full_name='algorithm.AlgorithmRequest.use_cache', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_ALGORITHMREQUEST_KWARGSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=194,
)


_ALGORITHMREPLY = _descriptor.Descriptor(
  name='AlgorithmReply',
  full_name='algorithm.AlgorithmReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='algorithm.AlgorithmReply.state', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='algorithm.AlgorithmReply.timestamp', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='algorithm.AlgorithmReply.app_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hdfs_path', full_name='algorithm.AlgorithmReply.hdfs_path', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='algorithm.AlgorithmReply.message', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=196,
  serialized_end=298,
)


_SPARKQUERYREQUEST = _descriptor.Descriptor(
  name='SparkQueryRequest',
  full_name='algorithm.SparkQueryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='algorithm.SparkQueryRequest.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=300,
  serialized_end=335,
)


_SPARKQUERYREPLY = _descriptor.Descriptor(
  name='SparkQueryReply',
  full_name='algorithm.SparkQueryReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='algorithm.SparkQueryReply.state', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='finalStatus', full_name='algorithm.SparkQueryReply.finalStatus', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=337,
  serialized_end=390,
)

_ALGORITHMREQUEST_KWARGSENTRY.containing_type = _ALGORITHMREQUEST
_ALGORITHMREQUEST.fields_by_name['kwargs'].message_type = _ALGORITHMREQUEST_KWARGSENTRY
DESCRIPTOR.message_types_by_name['AlgorithmRequest'] = _ALGORITHMREQUEST
DESCRIPTOR.message_types_by_name['AlgorithmReply'] = _ALGORITHMREPLY
DESCRIPTOR.message_types_by_name['SparkQueryRequest'] = _SPARKQUERYREQUEST
DESCRIPTOR.message_types_by_name['SparkQueryReply'] = _SPARKQUERYREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AlgorithmRequest = _reflection.GeneratedProtocolMessageType('AlgorithmRequest', (_message.Message,), {

  'KwargsEntry' : _reflection.GeneratedProtocolMessageType('KwargsEntry', (_message.Message,), {
    'DESCRIPTOR' : _ALGORITHMREQUEST_KWARGSENTRY,
    '__module__' : 'algorithm_pb2'
    # @@protoc_insertion_point(class_scope:algorithm.AlgorithmRequest.KwargsEntry)
    })
  ,
  'DESCRIPTOR' : _ALGORITHMREQUEST,
  '__module__' : 'algorithm_pb2'
  # @@protoc_insertion_point(class_scope:algorithm.AlgorithmRequest)
  })
_sym_db.RegisterMessage(AlgorithmRequest)
_sym_db.RegisterMessage(AlgorithmRequest.KwargsEntry)

AlgorithmReply = _reflection.GeneratedProtocolMessageType('AlgorithmReply', (_message.Message,), {
  'DESCRIPTOR' : _ALGORITHMREPLY,
  '__module__' : 'algorithm_pb2'
  # @@protoc_insertion_point(class_scope:algorithm.AlgorithmReply)
  })
_sym_db.RegisterMessage(AlgorithmReply)

SparkQueryRequest = _reflection.GeneratedProtocolMessageType('SparkQueryRequest', (_message.Message,), {
  'DESCRIPTOR' : _SPARKQUERYREQUEST,
  '__module__' : 'algorithm_pb2'
  # @@protoc_insertion_point(class_scope:algorithm.SparkQueryRequest)
  })
_sym_db.RegisterMessage(SparkQueryRequest)

SparkQueryReply = _reflection.GeneratedProtocolMessageType('SparkQueryReply', (_message.Message,), {
  'DESCRIPTOR' : _SPARKQUERYREPLY,
  '__module__' : 'algorithm_pb2'
  # @@protoc_insertion_point(class_scope:algorithm.SparkQueryReply)
  })
_sym_db.RegisterMessage(SparkQueryReply)


_ALGORITHMREQUEST_KWARGSENTRY._options = None

_ALGORITHM = _descriptor.ServiceDescriptor(
  name='Algorithm',
  full_name='algorithm.Algorithm',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=393,
  serialized_end=561,
  methods=[
  _descriptor.MethodDescriptor(
    name='ExecuteAlgorithm',
    full_name='algorithm.Algorithm.ExecuteAlgorithm',
    index=0,
    containing_service=None,
    input_type=_ALGORITHMREQUEST,
    output_type=_ALGORITHMREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SparkQueryState',
    full_name='algorithm.Algorithm.SparkQueryState',
    index=1,
    containing_service=None,
    input_type=_SPARKQUERYREQUEST,
    output_type=_SPARKQUERYREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ALGORITHM)

DESCRIPTOR.services_by_name['Algorithm'] = _ALGORITHM

# @@protoc_insertion_point(module_scope)