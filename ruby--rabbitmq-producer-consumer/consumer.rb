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

    # create a channel and queue for communication, and get the exchange
    channel = connection.create_channel
    queue = channel.queue(ENV['QUEUE_NAME'])

    queue.subscribe(block: true) do |delivery_info, metadata, payload|
        puts "Received: #{payload}"
    end
rescue Exception => e
    # catch-all for errors
    puts "Error: " + e.message
ensure
    # make sure any connections are closed
    connection.close if connection
end
