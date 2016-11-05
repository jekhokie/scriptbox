#!/bin/bash
#
# Purpose: Install and configure an Apache Spark instance. Note that this is a VERY
#          simple install and does not allow much configuration in terms of port numbers
#          and the like.
#
# Warning: This script installs all files/binaries into the current directory that it is run from.
#          It is obviously very much not recommended to use this method for a production setup.
#
# Environment settings - configure to match your environment
#
# SCALA_VERSION:        Version of Scala to install.
# SPARK_VERSION:        Version of Spark to install.
# SPARK_MASTER_IP:      IP address of the master instance. Note that this must be a routable and
#                       reachable hostname or IP address for all nodes.
# SPARK_SLAVE_IP:       Required only when "SPARK_IS_MASTER=false". IP address of the slave (this)
#                       instance. Note that this must be a routable/reachable IP address for all
#                       nodes to reach.
# SPARK_IS_MASTER:      True/false as to whether this should be a master node.
# SPARK_MEM:            General max memory allocation (min 512m).
# SPARK_DRIVER_MEM:     Max amount of memory that the driver can consume (min 512m).
# SPARK_WORKER_MEM:     Max amount of memory that workers have to give to executors (min 512m).
# SPARK_EXECUTOR_MEM:   Memory per executor (min 512m).
# SPARK_EXECUTOR_CORES: Maximum number of cores to allocate to executors (min 1).

SCALA_VERSION=2.11.8
SPARK_VERSION=2.0.1
SPARK_MASTER_IP="10.11.13.15"
SPARK_SLAVE_IP="10.11.13.15"
SPARK_IS_MASTER=true
SPARK_MEM=512m
SPARK_DRIVER_MEM=512m
SPARK_WORKER_MEM=512m
SPARK_EXECUTOR_MEM=512m
SPARK_EXECUTOR_CORES=1

# some variables required to make life easier
scalaPackage=scala-${SCALA_VERSION}.deb
rootDir=$(pwd)
sparkDir=spark-${SPARK_VERSION}-bin-hadoop2.7
sparkPackage="${sparkDir}.tgz"
linkArray=("start-master" "stop-master" "start-slave" "stop-slave")
linkRoot=/usr/sbin
sparkHome="${rootDir}/${sparkDir}"
envFile="${sparkHome}/conf/spark-env.sh"
jobFile="${sparkHome}/conf/spark-defaults.conf"

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

write_output "Starting Apache Spark installation"

write_output "General package management update..."
apt-get update &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Package management update complete."
else
    write_error "  Failed to make package management update."
fi

write_output "Installing JRE dependency..."
apt list --installed default-jre-headless -a 2>/dev/null | grep -i default-jre-headless &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  JRE dependency is already installed - no action required."
else
    sudo apt-get -y install default-jre-headless &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  JRE dependency installation complete."
    else
        write_error "  Something went wrong installing the JRE dependency."
    fi
fi

write_output "Installing Scala software version ${SCALA_VERSION}..."
apt list --installed scala -a 2>/dev/null | grep scala | grep ${SCALA_VERSION} &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Scala version ${SCALA_VERSION} is already installed - no action required."
else
    if [ ! -f $scalaPackage ]; then
        write_output "  Downloading Scala package..."
        wget http://downloads.lightbend.com/scala/${SCALA_VERSION}/${scalaPackage} &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "    Scala version ${SCALA_VERSION} download complete."
            write_output "  Installing Scala version ${SCALA_VERSION}..."
            dpkg -i $scalaPackage &>/dev/null
            
            if [ $? -eq 0 ]; then
                write_output "    Scala installation complete."
            else
                write_error "    Exception attempting to install Scala."
            fi
        else
            write_error "    Exception attempting to download Scala.."
        fi
    fi
fi

write_output "Installing Spark software version ${SPARK_VERSION}..."
if [ -d $sparkDir ]; then
    write_output "  Spark version ${SPARK_VERSION} is already installed - no action required."
else
    if [ ! -f $sparkPackage ]; then
        write_output "  Downloading Spark package..."
        wget http://d3kbcqa49mib13.cloudfront.net/${sparkPackage} &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "    Spark version ${SPARK_VERSION} download complete."
        else
            write_error "    Exception attempting to download Spark."
        fi
    fi

    write_output "  Extracting Spark version ${SCALA_VERSION}..."
    tar xzf $sparkPackage &>/dev/null
            
    if [ $? -eq 0 ]; then
        write_output "    Spark extraction complete."
    else
        write_error "    Exception attempting to extract Spark."
    fi
fi

write_output "Creating useful symlinks to control processes..."
for ((i=0; i<${#linkArray[@]}; i++)); do
    link=${linkArray[$i]}
    linkFile="${linkRoot}/${link}"
    write_output "  Creating '${link}' symlink..."

    if [ -L $linkFile ]; then
        write_output "    '${link}' symlink already exists - no action required."
    else
        ln -s "${rootDir}/${sparkDir}/sbin/${link}.sh" $linkFile &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "    '${link}' symlink created successfully."
        else
            write_error "    Exception attempting to create '${link}' symlink."
        fi
    fi
done

write_output "Setting configuration properties..."
configStr="#!/usr/bin/env bash\nSPARK_LOCAL_IP=${SPARK_SLAVE_IP}\nSPARK_MEM=${SPARK_MEM}\nSPARK_DRIVER_MEMORY=${SPARK_DRIVER_MEM}\nSPARK_WORKER_MEMORY=${SPARK_WORKER_MEM}\nSPARK_EXECUTOR_MEMORY=${SPARK_EXECUTOR_MEM}"
if [[ "x${SPARK_IS_MASTER}" == "xtrue" ]]; then
    configStr="${CONFIG_STR}\nSPARK_MASTER_HOST=${SPARK_MASTER_IP}"
fi

echo -e $configStr | tee $envFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Coniguration properties set successfully."
else
    write_error "  Exception attempting to set configuration properties."
fi

write_output "Ensuring env file is executable..."
chmod +x $envFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Successfully made env file executable."
else
    write_error "  Exception attempting to make the env file executable."
fi

write_output "Setting submit-job properties..."
jobConfigStr="spark.driver.memory=${SPARK_DRIVER_MEM}\nspark.executor.memory=${SPARK_EXECUTOR_MEM}\nspark.executor.cores=${SPARK_EXECUTOR_CORES}"
echo -e $jobConfigStr | tee $jobFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Submit-job properties set successfully."
else
    write_error "  Exception attempting to set submit-job properties."
fi

if [[ "x${SPARK_IS_MASTER}" == "xtrue" ]]; then
    write_output "Starting the master process..."
    ps -ef | grep -v grep | grep spark.*Master &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Master process is already running - no action required."
    else
        SPARK_HOME=$sparkHome start-master &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Started the master process successfully."
        else
            write_error "  Exception attempting to start the master process."
        fi
    fi
else
    write_output "Starting the slave/worker process and joining to the master..."
    ps -ef | grep -v grep | grep spark.*Worker &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Slave/worker process is already running - no action required."
    else
        SPARK_HOME=$sparkHome start-slave spark://${SPARK_MASTER_IP}:7077 &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Started the slave/worker process successfully."
        else
            write_error "  Exception attempting to start the slave/worker process."
        fi
    fi
fi

write_summary "========================================================================="
write_summary "Your Spark node configuration is complete!"
write_summary "Ensure that your 'SPARK_HOME' env var is set to '${sparkHome}'"
write_summary "  This is best done in the account '.bashrc' or '.bash_profile'"
write_summary ""
write_summary "Spark Version: ${SPARK_VERSION}"
write_summary "Log Directory: ${sparkHome}/logs"
if [[ "x${SPARK_IS_MASTER}" == "xtrue" ]]; then
    write_summary "Purpose:       MASTER Node"
    write_summary "Master Web UI: http://${SPARK_MASTER_IP}:8080"
    write_summary "Master Port:   7077"
    write_summary "REST Port:     6066"
else
    write_summary "Purpose:             SLAVE Node"
    write_summary "Connected to Master: ${SPARK_MASTER_IP}"
    write_summary "Slave Web UI:        http://${SPARK_SLAVE_IP}:8081"
fi
write_summary "If you wish to test functionality and you have at least 1 worker, you can run the following:"
write_summary ""
write_summary "    ${sparkHome}/bin/spark-submit \\\\"
write_summary "      --class org.apache.spark.examples.SparkPi \\\\"
write_summary "      --master spark://${SPARK_MASTER_IP}:7077 \\\\"
write_summary "      ${sparkHome}/examples/jars/spark-examples_2.11-${SPARK_VERSION}.jar"
write_summary ""
write_summary "To check on the status, navigate to the web UI: http://${SPARK_MASTER_IP}:8080/"
