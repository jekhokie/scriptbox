#!/bin/bash
#
# Purpose: Install and configure an Apache Kafka instance, including the ZooKeeper dependency.
#
# Warning: This script installs all files/binaries into the current directory that it is run from.
#          It is obviously very much not recommended to use this method for a production setup.
#
# Environment settings - configure to match your environment
#
# SCALA_VERSION:   Version of Scala - note that changing this may/may not result in this script breaking.
# KAFKA_VERSION:   Version of Kafka to install - changing this may/may not result in this script breaking.
# KAFKA_HEAP_OPTS: JVM tuning options for the Kafka JVM.

SCALA_VERSION=2.11
KAFKA_VERSION=0.10.1.0
KAFKA_HEAP_OPTS="-Xmx256M -Xms256M"

# some variable assignments
dir=$(pwd)
dependencies=("default-jre" "default-jdk")
kafkaDir=kafka_${SCALA_VERSION}-${KAFKA_VERSION}
kafkaPackage=${kafkaDir}.tgz
kafkaUrl=http://apache.claz.org/kafka/${KAFKA_VERSION}/${kafkaPackage}
binDir=${dir}/${kafkaDir}/bin
configDir=${dir}/${kafkaDir}/config
zkLogfile=${dir}/${kafkaDir}/logs/zookeeper.log
kafkaLogfile=${dir}/${kafkaDir}/logs/kafka.log

# output an informational message with green background/black text
function write_output {
    echo -e "\e[42m\e[30m[$(date)] -- ${1}\e[0m"
}

# output an informational message with yellow background/black text
function write_summary {
    echo -e "\e[43m\e[30m[$(date)] -- ${1}\e[0m"
}

# output an error with red background/black text
function write_error {
    echo -e "\e[41m\e[30m[$(date)] -- ERROR - ${1}\e[0m"
    echo -e "\e[41m\e[30m[$(date)] -- EXITING\e[0m"
    exit 1
}

write_output "Starting Apache Kafka installation"

write_output "General package management update..."
apt-get update &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Package management update complete."
else
    write_error "  Failed to make package management update."
fi

write_output "Installing software dependencies..."
for ((i=0; i<${#dependencies[@]}; i++)); do
    package=${dependencies[$i]}
    apt list --installed $package -a 2>/dev/null | grep -i $package &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  '${package}' dependency is already installed - no action required."
    else
        apt-get -y install $package &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  '${package}' dependency installation complete."
        else
            write_error "  Something went wrong installing the '${package}' dependency."
        fi
    fi
done

write_output "Installing Kafka version ${KAFKA_VERSION}..."
if [ -d $kafkaDir ]; then
    write_output "  Kafka version ${KAFKA_VERSION} is already installed - no action required."
else
    if [ ! -f $kafkaPackage ]; then
        write_output "  Downloading Kafka package..."
        wget $kafkaUrl &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "    Kafka version ${KAFKA_VERSION} download complete."
        else
            write_error "    Exception attempting to download Kafka."
        fi
    fi

    write_output "  Extracting Kafka version ${KAFKA_VERSION}..."
    tar xzf $kafkaPackage &>/dev/null
            
    if [ $? -eq 0 ]; then
        write_output "    Kafka extraction complete."
    else
        write_error "    Exception attempting to extract Kafka."
    fi
fi

write_output "Starting the ZooKeeper process..."
ps -ef | grep -v grep | grep zookeeper &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  ZooKeeper process is already running - no action required."
else
    ${binDir}/zookeeper-server-start.sh ${configDir}/zookeeper.properties >${zkLogfile} 2>&1 &

    if [ $? -eq 0 ]; then
        write_output "  Started the ZooKeeper process successfully."
    else
        write_error "  Exception attempting to start the ZooKeeper process."
    fi
fi

write_output "Starting the Kafka process..."
ps -ef | grep -v grep | grep kafka | grep server\.properties &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Kafka process is already running - no action required."
else
    KAFKA_HEAP_OPTS="${KAFKA_HEAP_OPTS}" ${binDir}/kafka-server-start.sh ${configDir}/server.properties >${kafkaLogfile} 2>&1 &

    if [ $? -eq 0 ]; then
        write_output "  Started the Kafka process successfully."
    else
        write_error "  Exception attempting to start the Kafka process."
    fi
fi

write_summary "========================================================================="
write_summary "Your Kafka node configuration is complete!"
write_summary ""
write_summary "  ZooKeeper Port: 2181"
write_summary "  ZooKeeper Log:  ${zkLogfile}"
write_summary "  Kafka Port:     9092"
write_summary "  Kafka Log:      ${kafkaLogfile}"
write_summary ""
write_summary "You should be able to create a topic named 'test' via the following:"
write_summary ""
write_summary "    ${binDir}/kafka-topics.sh --create \\\\"
write_summary "           --zookeeper localhost:2181 \\\\"
write_summary "           --replication-factor 1 \\\\"
write_summary "           --partitions 1 \\\\"
write_summary "           --topic test"
write_summary ""
write_summary "Then, send a test message to the topic 'test':"
write_summary ""
write_summary "    ${binDir}/kafka-console-producer.sh --broker-list localhost:9092 --topic test"
write_summary "    ...Type the following:"
write_summary "        some test here"
write_summary "        and another test"
write_summary "        <CRTL-C>"
write_summary ""
write_summary "And retrieve the test messages:"
write_summary ""
write_summary "    ${binDir}/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning"
write_summary "    ...Should output:"
write_summary "        some test here"
write_summary "        and another test"
write_summary "        <CRTL-C>"
