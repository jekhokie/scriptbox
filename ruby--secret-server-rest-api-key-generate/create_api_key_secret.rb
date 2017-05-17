#!/usr/bin/env ruby
#
# This is a script to auto-create an OAuth 1.0a REST API key in Secret Server. The key name
# and corresponding auto-generated password are stored and shared out to the user for which
# the key was requested.
#
# == Parameters
#
# * +user_id+      - The Active Directory ID of the user for which this secret is being created
# * +service_name+ - Name of the service that this user is having an API key generated for
#
# == Returns
#
# * +STRING+ - A string containing a direct link to the secret that has been generated (if successful)
#
# == Raises
#
# * +EXCEPTION+ - Raises an exception if any errors occur in communicating or auto-generating the secret
#
# == Refactor
#
# * Remove the hard-coded envelopes - yes this is bad, but the libraries to auto-populate
#   the data based on the WSDL are awful (bigger todo - yell at Thycotic to change their SOAP interface
#   to a sane REST interface).
# * Be more generic in method calls for better re-use - right now, this all hinges on creating a secret
#   of type "REST API Key" since the actual secret creation envelope is structured with this data.
# * DRY up code - there is a lot of duplication in here, especially around error handling/SOAP calls.
# * Figure out a way that the password can be auto-generated on secret create rather than explicitly making
#   a call to retrieve an auto-generated password and then setting it (might raise some security concerns).

require 'optparse'
require 'savon'
require 'yaml'

# ensure options provided match script signature
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: create_api_key_secret.rb [options]"

  opts.on('-u', '--userid USERID',           'User ID')      { |o| options[:user_id]      = o }
  opts.on('-s', '--servicename SERVICENAME', 'Service Name') { |o| options[:service_name] = o }
end.parse!

raise "Missing option: -u/--userid USERID" if options[:user_id].nil?
raise "Missing option: -s/--servicename SERVICENAME" if options[:service_name].nil?

# set up configurations
CONFIG               = YAML.load_file('config/settings.yml')
key_name_info        = CONFIG['key_name_field']
key_password_info    = CONFIG['key_password_field']
key_description_info = CONFIG['key_description_field']
secret_name          = "AUTOMATED_#{options[:user_id]}-#{options[:service_name]}"

begin
  # create the SOAP client
  client = Savon.client(wsdl: "#{CONFIG['secret_server']['base_url']}#{CONFIG['secret_server']['wsdl_path']}")

  # construct the token request envelope
  token_xml = <<-EOF
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:thesecretserver.com">
      <soapenv:Header/>
      <soapenv:Body>
        <urn:Authenticate>
          <urn:username>#{CONFIG['auth']['username']}</urn:username>
          <urn:password>#{CONFIG['auth']['password']}</urn:password>
          <urn:domain>#{CONFIG['auth']['domain']}</urn:domain>
        </urn:Authenticate>
      </soapenv:Body>
    </soapenv:Envelope>
  EOF

  # attempt to obtain the token
  token_response = client.call(:authenticate, xml: token_xml)

  # ensure the command to obtain a token succeeded - return an error if not
  if (errors = token_response.body[:authenticate_response][:authenticate_result][:errors]).nil?
    token = token_response.body[:authenticate_response][:authenticate_result][:token]
  else
    raise "An exception occurred attempting to obtain an access token: #{errors}"
  end

  # construct the auto-generated password envelope
  generate_password_xml = <<-EOF
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:thesecretserver.com">
      <soapenv:Header/>
      <soapenv:Body>
        <urn:GeneratePassword>
          <urn:token>#{token}</urn:token>
          <urn:secretFieldId>#{key_password_info['field_id']}</urn:secretFieldId>
        </urn:GeneratePassword>
      </soapenv:Body>
    </soapenv:Envelope>
  EOF

  # attempt to obtain an auto-generated password conforming to the API key format
  password_response = client.call(:generate_password, xml: generate_password_xml)

  # ensure the command to obtain an auto-generated password succeeded - return an error if not
  if (errors = password_response.body[:generate_password_response][:generate_password_result][:errors]).nil?
    key_password = password_response.body[:generate_password_response][:generate_password_result][:generated_password]
  else
    raise "An exception occurred attempting to obtain an auto-generated password: #{errors}"
  end

  # construct the create secret envelope
  create_secret_xml = <<-EOF
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:thesecretserver.com">
      <soapenv:Header/>
      <soapenv:Body>
        <urn:AddNewSecret>
          <urn:token>#{token}</urn:token>
          <urn:secret>
            <urn:Name>#{secret_name}</urn:Name>
            <urn:Items>
              <urn:SecretItem>
                <urn:Value>#{options[:user_id]}-#{options[:service_name]}</urn:Value>
                <urn:FieldId>#{key_name_info['field_id']}</urn:FieldId>
                <urn:FieldName>#{key_name_info['field_name']}</urn:FieldName>
                <urn:FieldDisplayName>#{key_name_info['field_display_name']}</urn:FieldDisplayName>
              </urn:SecretItem>
              <urn:SecretItem>
                <urn:Value>#{key_password}</urn:Value>
                <urn:FieldId>#{key_password_info['field_id']}</urn:FieldId>
                <urn:FieldName>#{key_password_info['field_name']}</urn:FieldName>
                <urn:FieldDisplayName>#{key_password_info['field_display_name']}</urn:FieldDisplayName>
              </urn:SecretItem>
              <urn:SecretItem>
                <urn:Value>This is an auto-generated OAuth 1.0a API key for '#{options[:user_id]}' to access the '#{options[:service_name]}' service.</urn:Value>
                <urn:FieldId>#{key_description_info['field_id']}</urn:FieldId>
                <urn:FieldName>#{key_description_info['field_name']}</urn:FieldName>
                <urn:FieldDisplayName>#{key_description_info['field_display_name']}</urn:FieldDisplayName>
              </urn:SecretItem>
            </urn:Items>
            <urn:SecretTypeId>#{CONFIG['settings']['secret_type_id']}</urn:SecretTypeId>
            <urn:FolderId>#{CONFIG['settings']['folder_id']}</urn:FolderId>
            <urn:SecretPermissions>
              <urn:CurrentUserHasView>true</urn:CurrentUserHasView>
              <urn:CurrentUserHasEdit>true</urn:CurrentUserHasEdit>
              <urn:CurrentUserHasOwner>true</urn:CurrentUserHasOwner>
              <urn:InheritPermissionsEnabled>false</urn:InheritPermissionsEnabled>
              <urn:IsChangeToPermissions>true</urn:IsChangeToPermissions>
              <urn:Permissions>
                <urn:Permission>
                  <urn:UserOrGroup>
                    <urn:Name>#{CONFIG['auth']['domain']}\\#{options[:user_id]}</urn:Name>
                    <urn:IsUser>true</urn:IsUser>
                  </urn:UserOrGroup>
                  <urn:View>true</urn:View>
                  <urn:Edit>false</urn:Edit>
                  <urn:Owner>false</urn:Owner>
                </urn:Permission>
                <urn:Permission>
                  <urn:UserOrGroup>
                    <urn:Name>#{CONFIG['auth']['domain']}\\#{CONFIG['auth']['username']}</urn:Name>
                    <urn:IsUser>true</urn:IsUser>
                  </urn:UserOrGroup>
                  <urn:View>true</urn:View>
                  <urn:Edit>true</urn:Edit>
                  <urn:Owner>true</urn:Owner>
                </urn:Permission>
              </urn:Permissions>
            </urn:SecretPermissions>
          </urn:secret>
        </urn:AddNewSecret>
      </soapenv:Body>
    </soapenv:Envelope>
  EOF

  # attempt to create the secret
  secret_response = client.call(:add_new_secret, xml: create_secret_xml)

  # ensure the command to create the secret succeeded - return an error if not
  if (errors = secret_response.body[:add_new_secret_response][:add_new_secret_result][:errors]).nil?
    secret_id = secret_response.body[:add_new_secret_response][:add_new_secret_result][:secret][:id]
  else
    raise "An exception occurred attempting to create the secret: #{errors}"
  end
rescue Savon::Error => err
  raise "Something went terribly wrong attempting to communicate with the API endpoint: #{err}"
end

# output the secret URL
secret_url = "#{CONFIG['secret_server']['base_url']}#{CONFIG['secret_server']['secret_path']}#{secret_id}"
puts "Link to Secret: #{secret_url}"
return secret_url
