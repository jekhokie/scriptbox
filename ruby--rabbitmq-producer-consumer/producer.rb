#!/usr/bin/env ruby

require 'dotenv'
require "bunny"

# load environment-specific configurations
Dotenv.load

begin
    # establish connection with RMQ
    connection = Bunny.new(hostname:     ENV['RMQ_HOST'],
                           port:         ENV['RMQ_PORT'],
                           username:     ENV['RMQ_USERNAME'],
                           password:     ENV['RMQ_PASSWORD'],
                           virtual_host: ENV['RMQ_VHOST'])
    connection.start

    puts "Connection Established..."
    puts "Host: #{ENV['RMQ_HOST']}"
    puts "Port: #{ENV['RMQ_PORT']}"
    puts "Username: #{ENV['RMQ_USERNAME']}"
    puts "Password: #{ENV['RMQ_PASSWORD'].gsub(/./, '*')}"
    puts "Virtual Host: #{ENV['RMQ_VHOST']}"
    puts "Queue: #{ENV['QUEUE_NAME']}"
    puts "--------------------------------"

    # create a channel and queue for communication, and get the exchange for publishing
    channel = connection.create_channel
    queue = channel.queue(ENV['QUEUE_NAME'])
    exchange = channel.default_exchange

    # send messages to the channel/queue
    while true do
        # calculate random data to send
        rand_num = rand(0..1000)
        puts "Sending '#{rand_num}' to queue"

        # send random data
        exchange.publish("#{rand_num}", routing_key: queue.name)

        # sleep for user-defined ms
        sleep(ENV['MESSAGE_SLEEP_MS'].to_f / 1000.0)
    end
rescue Exception => e
    # catch-all for errors
    puts "Error: " + e.message
ensure
    # make sure any connections are closed
    connection.close if connection
end
