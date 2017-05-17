#!/usr/bin/env ruby
#
# Jira Query
#
# Performs a user-specified JQL query against a Jira instance and returns the query results.
#

require "jira"
require "pp"
require "yaml"

# initialize configurations
CONFIG    = YAML.load_file("config/settings.yml") unless defined?(CONFIG)
jira_url  = CONFIG["jira"]["url"]
jira_user = CONFIG["jira"]["user"]
jira_pass = CONFIG["jira"]["pass"]
jql_query = CONFIG["jira"]["jql_query"]

# SSL verification is probably important
options = {
  username:     jira_user,
  password:     jira_pass,
  site:         jira_url,
  context_path: "/jira",
  auth_type:    :basic,
  ssl_verify_mode: OpenSSL::SSL::VERIFY_NONE
}

# create a new Jira client with the requested query
client  = JIRA::Client.new(options)
results = JIRA::Resource::Issue.jql(client, jql_query)

# output results
results.each do |result|
  pp result
end
