"""
Scheduler queues
"""
import marshal
import pickle
from os import PathLike
from pathlib import Path
from typing import Union
from queuelib import queue
from scrapy.utils.request import request_from_dict
_PickleFifoSerializationDiskQueue = _serializable_queue(_with_mkdir(queue.FifoDiskQueue), _pickle_serialize, pickle.loads)
_PickleLifoSerializationDiskQueue = _serializable_queue(_with_mkdir(queue.LifoDiskQueue), _pickle_serialize, pickle.loads)
_MarshalFifoSerializationDiskQueue = _serializable_queue(_with_mkdir(queue.FifoDiskQueue), marshal.dumps, marshal.loads)
_MarshalLifoSerializationDiskQueue = _serializable_queue(_with_mkdir(queue.LifoDiskQueue), marshal.dumps, marshal.loads)
PickleFifoDiskQueue = _scrapy_serialization_queue(_PickleFifoSerializationDiskQueue)
PickleLifoDiskQueue = _scrapy_serialization_queue(_PickleLifoSerializationDiskQueue)
MarshalFifoDiskQueue = _scrapy_serialization_queue(_MarshalFifoSerializationDiskQueue)
MarshalLifoDiskQueue = _scrapy_serialization_queue(_MarshalLifoSerializationDiskQueue)
FifoMemoryQueue = _scrapy_non_serialization_queue(queue.FifoMemoryQueue)
LifoMemoryQueue = _scrapy_non_serialization_queue(queue.LifoMemoryQueue)