#!/usr/bin/env python
#
# TODO Improvements:
#   * Error handling (there basically is none at the moment/assumes happy path)
#   * Supplement this script with a bash script/process that iterates collection over clusters
#       and produces the JSON files that this file expects to parse the data
#   * Drive cluster specification from configuration file
#   * Add replication factor to understand cost due to replicas
#   * Marry/merge log dirs output with topic describe data for enriching information
#   * Identify ownership of topics for cost attribution
#   * Get cluster information from query to determine how many nodes to calculate total cost
#
# Code Snippet Credits:
#   * Byte size conversions: https://gist.github.com/Pobux/0c474672b3acd4473d459d3219675ad8

import json
import math
import yaml
from operator import itemgetter
from os.path import exists

# load configs
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# check that the logdirs JSON file exists - else fail
if not exists(config["log_dirs_file"]):
    raise Exception("The JSON file containing the log dirs info '{}' does not exist".format(config["log_dirs_file"]))
    exit(1)

# some configurations for size conversions
BASE_SIZE = 1024.00
SIZE_NAME = ["B", "KB", "MB", "GB", "TB", "PB"]
def bytes_to_readable(size_bytes):
    '''
    Convert bytes to a higher-order size metric conversion that is readable
    '''

    current_size = size_bytes
    size_index = 0
    while current_size >= BASE_SIZE and len(SIZE_NAME) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    converted_size = "{:.3f}".format(current_size)
    size_measure = SIZE_NAME[size_index]

    return converted_size, size_measure

def parse_log_dirs():
    '''
    Parse the JSON file containing the partition logs for the topics captured
    '''

    topic_list = []

    # load from json
    with open(config["log_dirs_file"], "r") as f:
        logdir_data = json.load(f)

    # parse each topic partition and add them all up
    for broker in logdir_data['brokers']:
        for logdir in broker['logDirs']:
            for partition in logdir["partitions"]:
                # capture the topic name and current partition size
                topic_name = partition["partition"].rpartition('-')[0]
                part_size = partition["size"]

                # check if we already have the topic
                # if so, add partition size to it, else add new topic to list
                topic = next((topic for topic in topic_list if topic["name"] == topic_name), None)
                if topic is None:
                    topic_list.append({
                        "name": topic_name,
                        "size": part_size
                    })
                else:
                    topic["size"] += part_size

    # sort order the list for easier parsing
    return sorted(topic_list, key=itemgetter("size"), reverse=True)

def print_statistics(topic_list):
    '''
    Print interesting statistics about the topics captured
    '''

    # top 10 largest topics and associated sizes
    print("Cluster: {}".format(config["kafka_cluster"]))
    print("~~~~~~~~~~~~~~~~~")

    print("Top 10 Largest Topics")
    print("Note: This is total size, including replicated data (RF)")
    for topic in topic_list[:10]:
        if topic["size"] != 0:
            topic_size, measure = bytes_to_readable(topic["size"])
            print("    {} {} | {}".format(topic_size, measure, topic["name"]))

    print("~~~~~~~~~~~~~~~~~")

    # total number of topics
    sum_all_topics = len(topic_list)
    print("    # Topics Total: {}".format(sum_all_topics))

    # number of topics 1GB in size or more
    gb_topics = sum(topic["size"] >= (BASE_SIZE ** 3.0) for topic in topic_list)
    print("    # Topics 1GB or More in Size: {}".format(gb_topics))

    # number of topics with no data in them
    no_data_topics = sum(topic["size"] == 0 for topic in topic_list)
    print("    # Topics with No Data: {}".format(no_data_topics))

    # total size of all topics and replicas
    total_size_bytes = sum(topic["size"] for topic in topic_list)
    size, measure = bytes_to_readable(total_size_bytes)
    print("    Total Size of All Topics: {} {}".format(size, measure))

    print("~~~~~~~~~~~~~~~~~")

def main():
    '''
    Main execution method
    '''

    topic_list = parse_log_dirs()
    print_statistics(topic_list)

if __name__ == '__main__':
    main()
