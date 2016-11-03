#!/bin/bash

# Environment settings - configure to match your environment
# CLUSTER_FQDNS:   Fully-qualified domain names of the hosts in the cluster - make sure that
#                  the names are in fact fully qualified for your environment as this is the
#                  most capable way to accommodate successful clustering.
# MASTER_FQDN:     The FQDN of the master node - needed for cluster joining.
# IS_MASTER:       Whether this node should initially be the master - this is important to ONLY
#                  set on the first node created to ensure the cluster forms, the management
#                  plugin is only installed on one of the nodes, and the user/privs are configured
#                  as expected. Note that this *could* be circumvented via determining whether the
#                  current FQDN matches the MASTER_FQDN parameter, but there is no guarantee that
#                  the node FQDN matches the MASTER_FQDN (it can be different).
# ADMIN_PASSWORD:  Password desired for the 'admin' user to manage the RabbitMQ cluster.
#
CLUSTER_FQDNS="rabbit1.localhost,rabbit2.localhost,rabbit3.localhost"
MASTER_FQDN="rabbit1.localhost"
IS_MASTER=true
ADMIN_PASSWORD="admin"

# settings - update as necessary, but note that changing these may result in a non-operational cluster
RABBITMQ_VERSION=3.6.5-1
ULIMIT_SETTING=65536
ERLANG_COOKIE="somesupersecretpassphrase"
VM_MEM_HIGH_WATERMARK=0.8
DISK_FREE_LIMIT=0.5

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

write_output "Starting RabbitMQ installation"

# first-thing's first - all hostnames MUST be resolvable by the node in order
# for the clustering to work correctly, and assign the cluster format for
# future rabbitmq.config settings
write_output "Checking that all CLUSTER_FQDNs are resolvable..."
OIFS=$IFS
IFS=","
hostArray=($CLUSTER_FQDNS)
IFS=$OIFS
clusterHosts="["
for ((i=0; i<${#hostArray[@]}; i++)); do
    host=${hostArray[$i]}
    ping -c 1 $host &>/dev/null

    if [ $? -eq 0 ]; then
        if [[ $i < $((${#hostArray[@]} - 1)) ]]; then
            clusterHosts="${clusterHosts} '${host}',"
        else
            clusterHosts="${clusterHosts} '${host}' "
        fi
    else
        write_error "  Could not resolve host '$host' - all hosts must be able to resolve all others."
    fi
done
clusterHosts="${clusterHosts}]"

write_output "General package management update..."
apt-get update 2&>/dev/null
write_output "  Package management update complete."

write_output "Checking for Erlang dependency..."
apt list --installed erlang-nox -a 2>/dev/null | grep -i erlang &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Erlang dependency is already installed - no action required."
else
    write_output "  Erlang dependency not found - installing..."

    if [ ! -f erlang-solutions_1.0_all.deb ]; then
        wget http://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb &>/dev/null
    fi

    dpkg -i erlang-solutions_1.0_all.deb &>/dev/null
    apt-get update &>/dev/null
    apt-get -y install erlang-nox &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Erlang dependency installation complete."
    else
        write_error "  Something went wrong installing the Erlang dependency."
    fi
fi

write_output "Installing additional dependencies..."
apt list --installed socat -a 2>/dev/null | grep -i socat &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Additional dependencies already installed - no action required."
else
    apt-get -y install socat &>/dev/null
    write_output "  Additional dependency installation complete."
fi

write_output "Installing RabbitMQ software version ${RABBITMQ_VERSION}..."
apt list --installed rabbitmq-server -a 2>/dev/null | grep -i rabbitmq-server &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  RabbitMQ version ${RABBITMQ_VERSION} is already installed - no action required."
else
    if [ ! -e rabbitmq-server_${RABBITMQ_VERSION}_all.deb ]; then
        wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.5/rabbitmq-server_${RABBITMQ_VERSION}_all.deb &>/dev/null
    fi

    dpkg -i rabbitmq-server_${RABBITMQ_VERSION}_all.deb &>/dev/null

    # this command will likely fail due to lack of configuration files, which is OK for the install
    write_output "  RabbitMQ version ${RABBITMQ_VERSION} installed."
fi

write_output "Configuring ulimit settings..."
# ulimit settings increase (https://www.rabbitmq.com/production-checklist.html#resource-limits-file-handle-limit)
grep -q "ulimit -n ${ULIMIT_SETTING}" /etc/default/rabbitmq-server
if [ $? -eq 0 ]; then
    write_output "  Ulimit settings already set - no action required."
else
    echo "ulimit -n ${ULIMIT_SETTING}" >> /etc/default/rabbitmq-server

    if [ $? -eq 0 ]; then
        write_output "  Set ulimit for RabbitMQ server to ${ULIMIT_SETTING}."
    else
        write_error "  Exception attempting to set ulimit for RabbitMQ."
    fi
fi

write_output "Configuring Erlang cookie for clustering capabilities..."
# erlang cookie for clustering capabilities (https://www.rabbitmq.com/production-checklist.html#security-considerations-erlang-cookie)
cookieFile=/var/lib/rabbitmq/.erlang.cookie
grep -q "${ERLANG_COOKIE}" $cookieFile 2>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Erlang cookie already set - no action required."
else
    echo "${ERLANG_COOKIE}" > $cookieFile
    chmod 400 $cookieFile
    chown rabbitmq:rabbitmq $cookieFile

    if [ $? -eq 0 ]; then
        write_output "  Set Erlang cookie for RabbitMQ clustering capability."
    else
        write_error "  Exception attempting to set Erlang cookie for RabbitMQ."
    fi
fi

write_output "Configuring the RabbitMQ server via a rabbitmq.config file..."
# set resource limits (https://www.rabbitmq.com/production-checklist.html#resource-limits)
if [ -f /etc/rabbitmq/rabbitmq.config ]; then
    write_output "  rabbitmq.config already in place - no action required."
else
    echo -e "[
    {rabbit, [
        {cluster_partition_handling, autoheal},
        {disk_free_limit, {mem_relative, 0.5}},
        {vm_memory_high_watermark, 0.8},
        {cluster_nodes, {${clusterHosts}, disc}}
    ]}
]." > /etc/rabbitmq/rabbitmq.config

    if [ $? -eq 0 ]; then
        write_output "  Setting rabbitmq.config file complete."
    else
        write_error "  Exception attempting to configure the RabbitMQ rabbitmq.config file."
    fi
fi

write_output "Setting environment configurations..."
if [ -f /etc/rabbitmq/rabbitmq-env.conf ]; then
    write_output "  rabbitmq-env.conf already in place - no action required."
else
    echo "RABBITMQ_USE_LONGNAME=true" > /etc/rabbitmq/rabbitmq-env.conf

    if [ $? -eq 0 ]; then
        write_output "  Setting rabbitmq-env.conf file complete."
    else
        write_error "  Exception attempting to configure the RabbitMQ rabbitmq-env.conf file."
    fi
fi

write_output "Starting the RabbitMQ service..."
service rabbitmq-server restart
if [ $? -eq 0 ]; then
    write_output "  RabbitMQ process started successfully on host."
else
    write_error "  Exception attempting to start the RabbitMQ server (rabbitmq-server) - please investigate logs"
fi

# certain things should only occur on the master
if [ "${IS_MASTER}" == true ]; then
    # this could also be done via placing '[rabbitmq_management].' in the file /etc/rabbitmq/enabled_plugins
    # if this occurred prior to the startup of the application
    write_output "Enabling the management plugin..."
    rabbitmq-plugins enable rabbitmq_management &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  RabbitMQ management plugin successfully enabled."
    else
        write_error "  Exception attempting to enable the RabbitMQ management plugin"
    fi

    write_output "Creating admin user..."
    rabbitmqctl list_users | grep ^admin &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  'admin' user already exists - no action required."
    else
        rabbitmqctl add_user admin $ADMIN_PASSWORD &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "  'admin' user created with password '${ADMIN_PASSWORD}'"
        else
            write_error "  Exception attempting to create the 'admin' user."
        fi
    fi
    
    write_output "Configuring admin user permissions..."
    rabbitmqctl list_permissions | grep ^admin &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  'admin' user permissions already configured - no action required."
    else
        rabbitmqctl set_permissions -p / admin ".*" ".*" ".*" &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "  'admin' user created with password '${ADMIN_PASSWORD}'"
        else
            write_error "  Exception attempting to set the 'admin' user privileges."
        fi
    fi
    
    write_output "Granting admin user access to management interface..."
    rabbitmqctl list_users | grep ^admin | grep management &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  'admin' user 'management' tag already configured - no action required."
    else
        rabbitmqctl set_user_tags admin management &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "  'admin' user tag 'management' set"
        else
            write_error "  Exception attempting to set a 'management' tag for the 'admin' user."
        fi
    fi
    
    write_output "Granting admin user full administrative control..."
    rabbitmqctl list_users | grep ^admin | grep administrator &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  'admin' user 'administrator' tag already configured - no action required."
    else
        rabbitmqctl set_user_tags admin administrator &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "  'admin' user tag 'administrator' set"
        else
            write_error "  Exception attempting to set a 'administrator' tag for the 'admin' user."
        fi
    fi
else
    # this could also be done via placing '[rabbitmq_management_agent].' in the file
    # /etc/rabbitmq/enabled_plugins if this occurred prior to the startup of the application
    write_output "Enabling the management agent..."
    rabbitmq-plugins enable rabbitmq_management_agent &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  RabbitMQ management agent successfully enabled."
    else
        write_error "  Exception attempting to enable the RabbitMQ management agent"
    fi

    write_output "Attemping to join cluster..."
    write_output "  Stopping the RabbitMQ application..."
    rabbitmqctl stop_app &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Stopped the RabbitMQ application successfully."
        write_output "  Attempting to join the node to the cluster..."
        rabbitmqctl join_cluster rabbit@${MASTER_FQDN} &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Joined to the cluster via master '${MASTER_FQDN}' successfully."
            write_output "  Attempting to start the RabbitMQ application..."
            rabbitmqctl start_app &>/dev/null

            if [ $? -eq 0 ]; then
                write_output "  Successfully started the RabbitMQ application following cluster join."
            else
                write_error "    Exception attempting to start the RabbitMQ application following cluster join."
            fi
        else
            write_error "    Exception attempting to join this node to the cluster via master '${MASTER_FQDN}'."
        fi
    else
        write_error "    Exception attempting to stop the RabbitMQ application prior to cluster join."
    fi
fi

write_summary "========================================================================="
write_summary "Your RabbitMQ node configuration is complete!"
if [ "${IS_MASTER}" == true ]; then
    write_summary "You should be able to access the management interface via the following URL:"
    write_summary "    http://<FQDN_OR_IP>:15672"
    write_summary "Log into the interface using the credentials 'admin'/'${ADMIN_PASSWORD}'"
fi
