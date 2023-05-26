import codecs
import header
import logger
import numpy
import random

def readFromSharedMemory(shared_memory, process_id, entry_id):
    start = process_id * header.parallel_shared_memory_size_process + entry_id * header.parallel_shared_memory_size_entry
    size = int(shared_memory.buf[start])
    end = start + 1 + size

    if end >= header.parallel_shared_memory_size_total:
        logger.log_error("Shared memory segmentation fault")
        return ""

    return str(codecs.decode(shared_memory.buf[start + 1:end], "ascii"))

def setSeed(seed):
    random.seed(seed)
    numpy.random.seed(seed)

    return

def writeToSharedMemory(shared_memory, process_id, entry_id, data):
    data = str(data)
    start = process_id * header.parallel_shared_memory_size_process + entry_id * header.parallel_shared_memory_size_entry
    end = start + 1 + len(data)

    if end >= header.parallel_shared_memory_size_total:
        logger.log_error("Shared memory segmentation fault")
        return

    shared_memory.buf[start] = len(data)
    shared_memory.buf[start + 1:end] = codecs.encode(data, "ascii")

    return
