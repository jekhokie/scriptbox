#!/bin/bash
#
# Purpose: Install and configure a Redis instance with the latest stable version of Redis available.
#
# Note: This script does not stand up a clustered node but, rather, a standalone node. The script
#       may be updated at a future time to accommodate clustering if/when such a feature is something
#       that is desired.

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

write_output "Starting Redis installation"

write_output "General package management update..."
apt-get update &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Package management update complete."
else
    write_error "  Failed to make package management update."
fi

write_output "Installing additional dependencies..."
deps=("build-essential" "tcl")
for dep in "${deps[@]}"; do
    apt list --installed $dep -a 2>/dev/null | grep -i $dep &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Additional '${dep}' dependency already installed - no action required."
    else
        apt-get -y install $dep &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "  Additional '${dep}' dependency installation complete."
        else
            write_error "  Exception attempting to install additional dependency '${dep}'."
        fi
    fi
done

write_output "Downloading latest Redis package..."
redisPackage="redis-stable.tar.gz"
if [ -f $redisPackage ]; then
    write_output "  Redis package already in place - no action required."
else
    curl -sO http://download.redis.io/redis-stable.tar.gz

    if [ $? -eq 0 ]; then
        write_output "  Latest stable Redis package downloaded."
    else
        write_error "  Exception attempting to download latest stable Redis package."
    fi
fi

write_output "Extracting Redis package..."
if [ -d redis-stable ]; then
    write_output "  Redis package already extracted/in place - no action required."
else
    tar xzf $redisPackage &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Redis package extracted successfully."
    else
        write_error "  Exception attempting to extract Redis package."
    fi
fi

write_output "Building and installing Redis..."
which redis-server &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Redis Server binaries already installed - no action required."
else
    # move into the source directory
    pushd redis-stable &>/dev/null
    
    write_output "  Running 'make' to compile binaries..."
    make &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "    Successfully ran 'make'."
    else
        write_error "    Exception attempting to run the 'make' command."
    fi
    
    write_output "  Running 'make test' to ensure binaries were built correctly..."
    make test &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "    Successfully ran 'make test'."
    else
        write_error "    Exception attempting to run the 'make test' command."
    fi
    
    write_output "  Running 'make install' to install binaries on the system..."
    make install &>/dev/null
    if [ $? -eq 0 ]; then
        write_output "    Successfully ran 'make install'."
    else
        write_error "    Exception attempting to run the 'make install' command."
    fi
    
    # return to script directory
    popd &>/dev/null
fi

write_output "Creating the redis user..."
id -a redis &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Redis user already exists - no action required."
else
    adduser --system --group --no-create-home redis &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully created the redis user."
    else
        write_error "  Exception attempting to create the redis user."
    fi
fi

redisConfigDir=/etc/redis
write_output "Creating configuration directory '${redisConfigDir}'..."
if [ -d $redisConfigDir ]; then
    write_output "  Redis configuration directory already exists - no action required."
else
    mkdir $redisConfigDir

    if [ $? -eq 0 ]; then
        write_output "  Successfully created configuration directory."
    else
        write_error "  Exception attempting to create configuration directory."
    fi
fi

redisDir=/var/lib/redis
write_output "Creating base Redis directory '${redisDir}'..."
if [ -d $redisDir ]; then
    write_output "  Redis base directory already exists - no action required."
else
    mkdir $redisDir

    if [ $? -eq 0 ]; then
        write_output "  Successfully created base directory."
    else
        write_error "  Exception attempting to create base directory."
    fi
fi

write_output "Changing ownership of base Redis directory '${redisDir}' to 'redis:redis'..."
chown redis:redis $redisDir
if [ $? -eq 0 ]; then
    write_output "  Successfully changed ownership of base directory."
else
    write_error "  Exception attempting to changed ownership of base directory."
fi

write_output "Changing mode of base Redis directory '${redisDir}' to '770'..."
chmod 770 $redisDir
if [ $? -eq 0 ]; then
    write_output "  Successfully changed mode of base directory."
else
    write_error "  Exception attempting to changed mode of base directory."
fi

redisConfig=/etc/redis/redis.conf
write_output "Creating template configuration file '${redisConfig}'..."
if [ -f $redisConfig ]; then
    write_output "  Redis template configuration already exists - no action required."
else
    cp redis-stable/redis.conf $redisConfig

    if [ $? -eq 0 ]; then
        write_output "  Successfully created template configuration."
    else
        write_error "  Exception attempting to create template configuration."
    fi
fi

write_output "Setting the base directory in the redis.conf..."
grep '^dir' $redisConfig | grep "${redisDir}" &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Redis base directory already specified - no action required."
else
    sed -i 's/^dir.*/dir \/var\/lib\/redis/' $redisConfig &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully set base directory."
    else
        write_error "  Exception attempting to set base directory."
    fi
fi

logDir=/var/log/redis
write_output "Creating the logging directory..."
if [ -d $logDir ]; then
    write_output "  Redis log directory already exists - no action required."
else
    mkdir $logDir &>/dev/null
    
    if [ $? -eq 0 ]; then
        write_output "  Successfully created logging directory."
    else
        write_error "  Exception attempting to create log directory."
    fi
fi

write_output "Changing ownership of Redis log directory to 'redis:redis'..."
chown redis:redis $logDir
if [ $? -eq 0 ]; then
    write_output "  Successfully changed ownership of logging directory."
else
    write_error "  Exception attempting to changed ownership of logging directory."
fi

write_output "Changing mode of Redis log directory to '775'..."
chmod 775 $logDir
if [ $? -eq 0 ]; then
    write_output "  Successfully changed mode of logging directory."
else
    write_error "  Exception attempting to changed mode of logging directory."
fi

logFile="${logDir}/redis_6379.log"
write_output "Setting the log file in the redis.conf..."
grep '^logfile' $redisConfig | grep "${logFile}" &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Redis log file already specified - no action required."
else
    sed -i 's/^logfile.*/logfile \/var\/log\/redis\/redis_6379.log/' $redisConfig &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully set log file."
    else
        write_error "  Exception attempting to set log file."
    fi
fi

sysSpec=/etc/systemd/system/redis.service
write_output "Creating systemd service spec '${sysSpec}'..."
if [ -f $sysSpec ]; then
    write_output "  Systemd service spec already in place - no action required."
else
    echo -e "[Unit]
Description=Redis
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target" > $sysSpec

    if [ $? -eq 0 ]; then
        write_output "  Created systemd spec file successfully."
    else
        write_error "  Exception attempting to create systemd spec file."
    fi
fi

write_output "Setting the 'vm.overcommit_memory' sysctl parameter..."
sysctl vm.overcommit_memory | grep 1 &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Sysctl setting already applied - no action required."
else
    sysctl -w vm.overcommit_memory=1 &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully set sysctl vm.overcommit_memory."
    else
        write_error "  Exception attempting to set sysctl vm.overcommit_memory."
    fi

    echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully persisted 'vm.overcommit_memory' in /etc/sysctl.conf."
    else
        write_error "  Exception attempting to persist 'vm.overcommit_memory' in /etc/sysctl.conf."
    fi
fi

write_output "Getting tcp-backlog setting..."
tcpBacklog=$(grep 'tcp-backlog' $redisConfig | awk '{print $2}') &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Successfully retrieved TCP backlog configuration as '${tcpBacklog}'."
else
    write_error "  Exception attempting to retrieve TCP backlog setting from config."
fi

maxConnFile=/proc/sys/net/core/somaxconn
write_output "Setting TCP backlog setting in '${maxConnFile}'..."
grep $tcpBacklog $maxConnFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  TCP backlog already set to '${tcpBacklog}' - no action required."
else
    echo $tcpBacklog | sudo tee $maxConnFile &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully set TCP backlog setting."
    else
        write_error "  Exception attempting to set TCP backlog setting."
    fi
fi

write_output "Disabling 'THP' (Transparent Huge Pages)..."
hugepageKernFile=/sys/kernel/mm/transparent_hugepage/enabled
grep '\[never\]' $hugepageKernFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  THP already disabled - no action required."
else
    echo never | tee -a $hugepageKernFile &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully disabled THP."
    else
        write_error "  Exception attempting to disable THP."
    fi
fi

rcFile=/etc/rc.local
write_output "Ensuring 'THP' is disabled on reboots ('${rcFile}')..."
grep $hugepageKernFile $rcFile | grep never &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  THP already disabled on reboot - no action required."
else
    echo -e "if test -f ${hugepageKernFile}; then
    echo never | sudo tee -a ${hugepageKernFile}
fi" >> $rcFile

    if [ $? -eq 0 ]; then
        write_output "  Successfully disabled THP on reboots."
    else
        write_error "  Exception attempting to disable THP on reboots."
    fi
fi

write_output "Configuring ulimit settings for redis user..."
ulimitFile=/etc/security/limits.conf
grep "redis soft nofile" $ulimitFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Ulimit settings already configured for redis user- no action required."
else
    echo -e "redis soft nofile 65535
redis hard nofile 65535" | sudo tee -a $ulimitFile &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Ulimit settings for redis user configured."
    else
        write_error "  Exception attempting to configure ulimit settings for redis user."
    fi
fi

write_output "Configuring PAM for new session ulimit application..."
pamFile=/etc/pam.d/common-session
grep "session\s*required\s*pam_limits.so" $pamFile &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  PAM settings already in place - no action required."
else
    echo "session required pam_limits.so" | sudo tee -a $pamFile &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully configured PAM for new sessions."
    else
        write_error "  Exception attempting to configure PAM for new sessions."
    fi
fi

write_output "Starting the Redis server..."
systemctl status redis &>/dev/null
if [ $? -eq 0 ]; then
    write_output "  Redis already running - no action required.."
else
    systemctl start redis &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "  Successfully started the Redis process."
    else
        write_error "  Exception attempting to start the Redis process."
    fi
fi

write_output "Verifying Redis is operating as expected..."

write_output "  Sending ping command..."
testKey="test"
testKeyVal="resultset"
redis-cli PING | grep PONG &>/dev/null
if [ $? -eq 0 ]; then
    write_output "    Redis ping responded successfully."

    write_output "  Setting a test key..."
    redis-cli set $testKey $testKeyVal &>/dev/null

    if [ $? -eq 0 ]; then
        write_output "    Redis set key responded successfully."

        write_output "  Getting test key..."
        redis-cli get $testKey | grep $testKeyVal &>/dev/null

        if [ $? -eq 0 ]; then
            write_output "    Redis get key responded successfully with correct value."
        else
            write_error "    Exception attempting to get test key.."
        fi
    else
        write_error "    Exception attempting to set test key.."
    fi
else
    write_error "    Exception attempting to ping Redis instance."
fi

write_summary "=========================================================================            "
write_summary "Your Redis node configuration is complete!                                           "
write_summary "You should be able to start using the Redis instance with the following information: "
write_summary "    Port:          6379                                                              "
write_summary "    Log Directory: ${logDir}                                                    "
write_summary "    Log File:      ${logFile}                                     "
