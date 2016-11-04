#!/bin/bash
#
# Purpose: Install and configure a Sensu server instance. Note that this installation will
#          assume a "standalone" configuration with respect to the API service running on
#          the same host unless the "API_HOST" parameter is changed to something other than
#          "localhost". In addition, a client will automatically be configured/started unless
#          the respective parameter is defined as false to prevent it.
#
# Environment settings - configure to match your environment
# 
# RABBITMQ_HOST:     FQDN or IP address of the RabbitMQ endpoint.
# RABBITMQ_PORT:     Port where the RabbitMQ process is listening.
# RABBITMQ_VHOST:    vhost to use for RabbitQM.
# RABBITMQ_USER:     User to use when communicating with RabbitMQ.
# RABBITMQ_PASSWORD: Password to use when communicating with RabbitMQ.
# REDIS_HOST:        FQDN or IP address of the Redis data store endpoint.
# REDIS_PORT:        Port where the Redis process is listening.
# API_HOST:          FQDN or IP address of where the API runs/will run. Change this to something
#                    other than "localhost" if you are/wish to run the API service on a separate
#                    host from the Sensu server host.
# API_BIND:          Bind address for the API service.
# API_PORT:          Port where the API service will bind/listen.
# ENABLE_CLIENT:     Whether the Sensu Client should be configured/started.
# ENABLE_UCHIWA:     Whether to install Uchiwa (web front-end) for Sensu.
# UCHIWA_BIND:       Uchiwa bind address - should likely remain 0.0.0.0.
# UCHIWA_PORT:       Port to have the Uchiwa instance listen on.
# UCHIWA_SENSU_NAME: Name to identify the Sensu instance.
# UCHIWA_SENSU_HOST: Host that the Sensu instance is listening on (usually localhost).
# UCHIWA_SENSU_PORT: Port that the Sensu API is listening on - should match API_PORT.

RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5671
RABBITMQ_VHOST=/
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
API_HOST=localhost
API_BIND=0.0.0.0
API_PORT=4567
ENABLE_CLIENT=true
ENABLE_UCHIWA=true
UCHIWA_HOST=0.0.0.0
UCHIWA_PORT=3000
UCHIWA_SENSU_NAME=Local_Sensu
UCHIWA_SENSU_HOST=localhost
UCHIWA_SENSU_PORT=4567

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

write_output "Starting Sensu installation"

write_output "Installing the Sensu packages..."
apt list --installed sensu -a 2>/dev/null | grep -i sensu &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Sensu server already installed - no action required."
else
    write_output "  Downloading and adding GPG public key required..."
    apt-key list | grep "Freight" &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "    GPG Key already loaded - no action required."
    else
        wget -q https://sensu.global.ssl.fastly.net/apt/pubkey.gpg -O- | sudo apt-key add - &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "    Successfully downloaded and added GPG key."
            else
            write_error "    Exception attempting to download and added GPG key."
        fi
    fi
    
    write_output "  Creating APT configuration file..."
    aptFile=/etc/apt/sources.list.d/sensu.list
    if [ -f $aptFile ]; then
        write_output "    APT file already created - no action required."
    else
        echo "deb     https://sensu.global.ssl.fastly.net/apt sensu main" | sudo tee $aptFile &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "    Successfully created APT file."
            else
            write_error "    Exception attempting to create APT file."
        fi
    fi
    
    write_output "  General package management update..."
    apt-get update &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "    Package management update complete."
    else
        write_error "    Failed to make package management update."
    fi
    
    write_output "  Installing the Sensu packages..."
    apt list --installed sensu -a 2>/dev/null | grep -i sensu &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "    Sensu server already installed - no action required."
    else
        apt-get -y install sensu &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "    Sensu server installation completed successfully."
        else
            write_error "    Exception attempting to install Sensu server."
        fi
    fi
fi

configDir=/etc/sensu/conf.d
clientConfig="${configDir}/client.json"
write_output "Creating client configuration '${clientConfig}'..."
if [ -f $clientConfig ]; then
    write_output "  Client configuration already in place - no action required."
else
    echo -e "{
  \"client\": {
    \"name\": \"localhost\",
    \"address\": \"127.0.0.1\",
    \"environment\": \"development\",
    \"subscriptions\": []
  }
}" > $clientConfig

    if [ $? -eq 0 ]; then
        write_output "  Successfully created client configuration file."
    else
        write_error "  Exception attempting to create client configuration file."
    fi
fi

transportConfig="${configDir}/transport.json"
write_output "Creating transport configuration '${transportConfig}'..."
if [ -f $transportConfig ]; then
    write_output "  Transport configuration already in place - no action required."
else
    echo -e "{
  \"transport\": {
    \"name\": \"rabbitmq\",
    \"host\": \"${RABBITMQ_HOST}\",
    \"port\": ${RABBITMQ_PORT},
    \"vhost\": \"${RABBITMQ_VHOST}\",
    \"user\": \"${RABBITMQ_USER}\",
    \"password\": \"${RABBITMQ_PASSWORD}\",
    \"heartbeat\": \"30\",
    \"prefetch\": \"10\",
    \"reconnect_on_error\": true
  }
}" > $transportConfig

    if [ $? -eq 0 ]; then
        write_output "  Successfully created transport configuration file."
    else
        write_error "  Exception attempting to create transport configuration file."
    fi
fi

datastoreConfig="${configDir}/redis.json"
write_output "Creating data store configuration '${datastoreConfig}'..."
if [ -f $datastoreConfig ]; then
    write_output "  Data store configuration already in place - no action required."
else
    echo -e "{
  \"redis\": {
    \"host\": \"${REDIS_HOST}\",
    \"port\": ${REDIS_PORT}
  }
}" > $datastoreConfig

    if [ $? -eq 0 ]; then
        write_output "  Successfully created data store configuration file."
    else
        write_error "  Exception attempting to create data store configuration file."
    fi
fi

apiConfig="${configDir}/api.json"
write_output "Creating API configuration '${apiConfig}'..."
if [ -f $apiConfig ]; then
    write_output "  API configuration already in place - no action required."
else
    echo -e "{
  \"api\": {
    \"host\": \"${API_HOST}\",
    \"bind\": \"${API_BIND}\",
    \"port\": ${API_PORT}
  }
}" > $apiConfig

    if [ $? -eq 0 ]; then
        write_output "  Successfully created API configuration file."
    else
        write_error "  Exception attempting to create API configuration file."
    fi
fi

testCheck="${configDir}/test_check.json"
write_output "Creating test check definition '${testCheck}'..."
if [ -f $testCheck ]; then
    write_output "  Test check already in place - no action required."
else
    echo -e "{
  \"checks\": {
    \"test\": {
      \"command\": \"echo -n OK\",
      \"interval\": 30,
      \"standalone\": true
    }
  }
}" > $testCheck

    if [ $? -eq 0 ]; then
        write_output "  Successfully created test check file."
    else
        write_error "  Exception attempting to create test check file."
    fi
fi

write_output "Enabling Sensu server on system boot..."
find /etc/rc*.d/ -name *sensu-server  | grep sensu &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Sensu API server already enabled on boot - no action required."
else
    update-rc.d sensu-server defaults &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully enabled Sensu server on boot."
    else
        write_error "  Exception attempting to enable Sensu server on boot."
    fi
fi

write_output "Assigning correct permissions on Sensu directory..."
chown -R sensu:sensu /etc/sensu &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Successfully assigned permissions to directory."
else
    write_error "  Exception attempting to assign ownership permissions of directory."
fi

write_output "Starting the Sensu server..."
service sensu-server status &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Sensu server already running - no action required."
else
    service sensu-server start &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully started Sensu server."
    else
        write_error "  Exception attempting to start Sensu server."
    fi
fi

if [[ "x${API_HOST}" == "xlocalhost" ]]; then
    write_output "Enabling API service on system boot..."
    find /etc/rc*.d/ -name *sensu-api | grep sensu-api &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Sensu API service already enabled on boot - no action required."
    else
        update-rc.d sensu-api defaults &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Successfully enabled Sensu API on boot."
        else
            write_error "  Exception attempting to enable Sensu API on boot."
        fi
    fi

    write_output "Starting the API service..."
    service sensu-api status &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Sensu API service already running - no action required."
    else
        service sensu-api start &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Successfully started Sensu API service."
        else
            write_error "  Exception attempting to start Sensu API service."
        fi
    fi

    write_output "Verifying the API service..."
    curl -s http://127.0.0.1:4567/clients | grep localhost &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Sensu API service verification successful."
    else
        write_error "  Exception attempting to verify the Sensu API service."
    fi
fi

if [[ "x${ENABLE_CLIENT}" == "xtrue" ]]; then
    write_output "Enabling client service on system boot..."
    find /etc/rc*.d/ -name *sensu-client | grep sensu-client &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Sensu client service already enabled on boot - no action required."
    else
        update-rc.d sensu-client defaults &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Successfully enabled Sensu client on boot."
        else
            write_error "  Exception attempting to enable Sensu client on boot."
        fi
    fi

    write_output "Starting the Sensu client service..."
    service sensu-client status &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Sensu client service already running - no action required."
    else
        service sensu-client start &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Successfully started Sensu client service."
        else
            write_error "  Exception attempting to start Sensu client service."
        fi
    fi
fi

if [[ "x${ENABLE_UCHIWA}" == "xtrue" ]]; then
    write_output "Installing the Uchiwa packages..."
    apt list --installed uchiwa -a 2>/dev/null | grep -i uchiwa &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "  Uchiwa already installed - no action required."
    else
        apt-get -y install uchiwa &>/dev/null
    
        if [ $? -eq 0 ]; then
            write_output "  Uchiwa installation completed successfully."
        else
            write_error "  Exception attempting to install Uchiwa."
        fi
    fi

    write_output "Configuring Uchiwa..."
    uchiwaConfig=/etc/sensu/uchiwa.json
    grep $UCHIWA_SENSU_NAME $uchiwaConfig &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Uchiwa already configured - no action required."
    else
        echo -e "{
  \"sensu\": [
    {
      \"name\": \"${UCHIWA_SENSU_NAME}\",
      \"host\": \"${UCHIWA_SENSU_HOST}\",
      \"port\": ${UCHIWA_SENSU_PORT}
    }
  ],
  \"uchiwa\": {
    \"host\": \"${UCHIWA_HOST}\",
    \"port\": ${UCHIWA_PORT}
  }
}" | sudo tee $uchiwaConfig &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "    Uchiwa configuration completed successfully."
        else
            write_error "    Exception attempting to configure Uchiwa."
        fi
    fi

    write_output "Starting the Uchiwa service..."
    service uchiwa status &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Uchiwa service already running - no action required."
    else
        service uchiwa start &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Successfully started Uchiwa service."
        else
            write_error "  Exception attempting to start Uchiwa service."
        fi
    fi
fi

write_summary "==========================================="
write_summary "Your Sensu configuration is complete!"
write_summary "Details related to your installation:"
write_summary ""
write_summary "  Sensu Server [installed]"

if [[ "x${API_HOST}" == "xlocalhost" ]]; then
    write_summary "  Sensu API [installed]"
    write_summary "    Bound To:          ${API_BIND}"
    write_summary "    Listening on Port: ${API_PORT}"
fi

if [[ "x${ENABLE_CLIENT}" == "xtrue" ]]; then
    write_summary "  Sensu Client [installed]"
fi

if [[ "x${ENABLE_UCHIWA}" == "xtrue" ]]; then
    write_summary "  Uchiwa [installed]"
    write_summary "    Bound To:          ${UCHIWA_HOST}"
    write_summary "    Listening on Port: ${UCHIWA_PORT}"
    write_summary "    To Access: http://<IP_OF_VM>:3000/"
fi
write_summary ""
write_summary "In addition, a local/standalone check has been configured:"
write_summary "  Local/standalone check: 'test'"
write_summary ""
write_summary "If you'd like to manually trigger a failure of the above check, run this command:"
write_summary ""
write_summary "  echo '{ \"name\": \"test\", \"output\": \"fail\", \"status\": 2 }' | nc localhost 3030"
write_summary ""
write_summary "Following execution, you should be able to see the check fail in the Uchiwa interface."
