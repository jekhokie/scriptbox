# Jira Query

Python script that, given a Jira project and issue type, will query Jira for all issues that
match and perform some basic calculations for determining efficiency by teams working in the
Jira project. Various metrics such as total issues, closed issues, average time to close, etc.
are produced, and a CSV output that can be used for further investigation on a per-ticket basis.

**Note**: This has NOT been tested against a project that has multiple tens of thousands of issues, so
your mileage may vary, but it is a decent starting point for some programmatic inspection of Jira projects.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--jira-query/
```

Install the required environment and libraries:

```bash
$ python3 -m virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Create a configuration file from the sample and specify the values for your specific environment.
This particular configuration will be our source for the Jira API specifications:

```bash
$ cp config/settings.yml.sample config/settings.yml
# edit the config/settings.yml file for your environment
```

**WARNING**: You will likely want to lock down the `settings.yml` file as it will contain sensitive
information - better yet, just switch the code to use environment variables so you don't need to
worry about storing such sensitive info!

## Usage

Now that the configurations are in place, run the script to query the Jira project and produce some
useful output:

```bash
$ ./query_jira_stats.py
```

If all goes well, you should see some metrics output and a file produced to the resulting output directory
which is a CSV that can be used for further investigation. Run the `help` switch of the command-line
tool to get some other useful ways to interact with the script such as verbose mode to print out the
resulting JSON structure, or force mode which forces Jira to be re-queried for an updated list of issues
(by default, a local cached serialized version of the issues is used to speed up local development and
testing).
