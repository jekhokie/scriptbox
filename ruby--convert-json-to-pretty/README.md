# Convert JSON to Pretty

This script takes a JSON file as input and converts the JSON data/prints the JSON
data to a pretty format (spacing, indentation, etc) in an output file.

## Prerequisites

Install RVM according to the installation instructions on the website:

- https://rvm.io/

Install bundler:

```bash
gem install bundler
```

Install the required gems:

```bash
bundle install
```

## Executing

Run the script and pass a valid JSON document that you wish to have re-formatted in a new file.
Note the 'sample.json' file in the base directory provides an example of how this works.

```bash
bundle exec ruby convert_json_to_pretty.rb sample.json
# inspect the resulting output file 'sample_pretty.json'
```
