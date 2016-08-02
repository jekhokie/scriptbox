# Test Unit Completion

A good Ruby test name will often times include a sentence that is fairly long in length. This makes it
cumbersome to run a specific test from the command line due to the fact that the user must type out the
entire test name separated by underscores.

test-unit-completion allows tab-completion of the test names for Test::Unit tests based on the file
provided within the command-line test command, thus helping to avoid typos and aid the user in signifying
the test that they wish to run.

## Install

Copy the completion script to the bash_completion.d directory:

```bash
cp test-unit /etc/bash_completion.d/
```

Source the bash_completion file to load the new completion rules:

```bash
source /etc/bash_completion
```

## Usage

In order to use the test-unit bash completion capability, utilize the normal Test::Unit syntax from the
command line. After typing the test name specifier switch '-n', hit <TAB> twice:

```bash
ruby -Itest test/unit/foo_test.rb -n test_should<TAB><TAB>
```

Once tab is pressed twice, a listing of all possible test options will be shown and can be used
for auto-completion.
