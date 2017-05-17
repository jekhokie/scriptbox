#!/usr/bin/env ruby
#
# This is a script to perform various operations through Thycotic Secret Server. It is intended
# to serve as a knowledge repository for basic ways in which SOAP interaction with Secret Server
# can be performed.
#
# == Outputs
#
# * +STRING+ - Many different print statements will result in different output throughout the script
#
# == Raises
#
# * +EXCEPTION+ - Raises an exception if any errors occur in communicating with Secret Server

require 'savon'
require 'yaml'

# set up configurations
CONFIG = YAML.load_file('config/settings.yml')

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
    puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    puts "API token obtained: #{token}"
    puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  else
    raise "An exception occurred attempting to obtain an access token: #{errors}"
  end

  # construct the envelope to obtain the "Generic Account" template fields
  get_template_fields_xml = <<-EOF
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:thesecretserver.com">
      <soap:Header/>
      <soap:Body>
        <urn:GetSecretTemplateFields>
          <urn:token>#{token}</urn:token>
          <urn:secretTypeId>#{CONFIG['settings']['secret_type_id']}</urn:secretTypeId>
        </urn:GetSecretTemplateFields>
      </soap:Body>
    </soap:Envelope>
EOF

  # attempt to get the fields for the defined template
  template_fields_response = client.call(:get_secret_template_fields, xml: get_template_fields_xml)

  # ensure the command to obtain the template fields succeeded - return an error if not
  if (errors = template_fields_response.body[:get_secret_template_fields_response][:get_secret_template_fields_result][:errors]).nil?
    template_fields = template_fields_response.body[:get_secret_template_fields_response][:get_secret_template_fields_result][:fields]
    puts "Template fields obtained: #{template_fields}"
    puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  else
    raise "An exception occurred attempting to obtain the template fields: #{errors}"
  end

  # construct the envelope to obtain a listing of all folders
  get_folder_xml = <<-EOF
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:thesecretserver.com">
      <soap:Header/>
      <soap:Body>
        <urn:SearchFolders>
          <urn:token>#{token}</urn:token>
          <urn:folderName>#{CONFIG['settings']['folder_name']}</urn:folderName>
        </urn:SearchFolders>
      </soap:Body>
    </soap:Envelope>
EOF

  # attempt to get the listing of all folders
  folder_response = client.call(:search_folders, xml: get_folder_xml)

  # ensure the command to obtain all folders succeeded - return an error if not
  if (errors = folder_response.body[:search_folders_response][:search_folders_result][:errors]).nil?
    folder = folder_response.body[:search_folders_response][:search_folders_result][:folders]
    puts "Folder obtained: #{folder}"
    puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  else
    raise "An exception occurred attempting to obtain the folder: #{errors}"
  end

  # construct the envelope to obtain a listing of all templates
  get_templates_xml = <<-EOF
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:thesecretserver.com">
      <soap:Header/>
      <soap:Body>
        <urn:GetSecretTemplates>
          <urn:token>#{token}</urn:token>
        </urn:GetSecretTemplates>
      </soap:Body>
    </soap:Envelope>
EOF

  # attempt to get the listing of all folders
  templates_response = client.call(:get_secret_templates, xml: get_templates_xml)

  # ensure the command to obtain all folders succeeded - return an error if not
  if (errors = templates_response.body[:get_secret_templates_response][:get_secret_templates_result][:errors]).nil?
    templates = templates_response.body[:get_secret_templates_response][:get_secret_templates_result][:secret_templates]
    puts "Number of templates obtained: #{templates.count}"
    puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    if (template = templates[:secret_template].select{ |template| template[:name] == CONFIG['settings']['template_name'] }[0]).nil?
      raise "Could not find a template with the name '#{CONFIG['settings']['template_name']}'"
    else
      puts "Template obtained: #{template}"
      puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    end
  else
    raise "An exception occurred attempting to obtain a list of all templates or the template being searched for: #{errors}"
  end
rescue Savon::Error => err
  raise "Something went terribly wrong attempting to communicate with the API endpoint: #{err}"
end
