import codecs
import header
import logger
import natsort
import numpy
import random

def getLabelsAttribute(dataset_config):
    labels_attribute = {}

    for attribute in dataset_config["attributes"]:
        if "" in attribute["labels"]:
            attribute["labels"].remove("")

        labels_attribute[attribute["name"]] = attribute["labels"]

    return labels_attribute

def getLabelsOriginal(dataset_config):
    return list(dataset_config["mappings"].keys())

def getLabelsOriginalInstanceWise(dataset_config):
    labels_original = []
    labels_original_set = set()

    for image_name in dataset_config["mappings"].keys():
        class_name = image_name.split('/')[0]

        if class_name not in labels_original_set:
            labels_original.append(class_name)
            labels_original_set.add(class_name)

    return natsort.natsorted(labels_original)

def getIndicesFromLabelsAttribute(labels_attribute):
    indices = {}

    for attribute in labels_attribute.keys():
        labels_to_indices = {}

        for i in range(len(labels_attribute[attribute])):
            labels_to_indices[labels_attribute[attribute][i]] = i

        indices[attribute] = labels_to_indices

    return indices

def getIndicesFromLabelsOriginal(labels_original):
    labels_to_indices = {}

    for i in range(len(labels_original)):
        labels_to_indices[labels_original[i]] = i

    return labels_to_indices

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

def shuffleUniform(list, seed):
    rand = random.Random()
    rand.seed(seed)
    rand.shuffle(list)

    return list

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
