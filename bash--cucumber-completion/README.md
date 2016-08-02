# Cucumber Completion

Cucumber provides great testing capability. However, you may not always want to run the entire feature,
at which point you might open the file, find the line number of the Scenario you wish to run, and then
append that to the end of the filename of the feature to be run. This hinter script provides the capability
to skip searching for the line number within a cucumber feature file and, rather, choose from a listing of
specified line numbers and their corresponding Scenarios right from the command line.

## Install

Copy the hinter script to the bash_completion.d directory:

```bash
cp test-cucumber /etc/bash_completion.d/
```

Source the bash_completion file to load the new hinter rules:

```bash
source /etc/bash_completion
```

## Usage

In order to use the cucumber bash hinter capability for running a particular Scenario, utilize the normal
Cucumber syntax from the command line. However, after specifying the filename of the feature followed by
a colon ':' indicating that you wish to enter a line number, press the tab key twice (such as in tab-completion):

```bash
cucumber my_nifty_test.feature:<tab><tab>
```

Performing the above (pressing tab twice for a traditional auto-complete of a filename, etc.) will result
in an output of line numbers and corresponding Scenario names of Scenarios within the feature test file
specified, like so:

```bash
       LN   TEST
    -----   -----------------------------------
       12   View existing stuff
       15   Edit a thing
       20   Edit a thing's thing
       26   Create a new thing
       32   Delete an existing thing

    POSSIBLE LINE NUMBERS:

    12  15  20  26  32
```

At this point, choose the line number of the Scenario you wish to run and type it after the colon within
the cucumber command (as normal), and off you go.
