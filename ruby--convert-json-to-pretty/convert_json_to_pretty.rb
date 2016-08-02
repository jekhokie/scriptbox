#!/usr/bin/env ruby
#
# This script takes a file containing JSON data and outputs the data to a new
# file in a pretty format (indentations, etc) for better readability.
#
# Usage:
#   ./convert_json_to_pretty <JSON_FILE>
#
# Where:
#   <JSON_FILE> is a valid file containing JSON structured data
#

require 'json'

# ensure a filename parameter is passed
raise "You must provide a valid filename as the first argument to this script" unless (file_name = ARGV[0])

# check if the file exists first
if File.exist?(file_name)
  # initialize variables
  base_name = File.basename(file_name, ".*")
  new_name  = "#{base_name}_pretty.json"

  # attempt to parse the file contents as JSON
  contents     = File.open(file_name)
  json_content = JSON.parse(contents.read)

  # write the JSON data as pretty-formatted to a new file, and inform the user
  File.open(new_name, "w") { |f| f.write(JSON.pretty_generate(json_content)) }

  puts "\n==================================================="
  puts "Pretty conversion of file '#{file_name}' successful"
  puts "Please inspect the following file: '#{new_name}'"
  puts "===================================================\n\n"
else
  raise "File '#{file_name}' not found"
end
