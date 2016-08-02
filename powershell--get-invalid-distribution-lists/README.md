# Invalid Distribution Lists

This script functionality detects and populates a CSV with information about 'invalid' groups
in Active Directory. See the specific script for details.

## Prerequisites

In order to run this script, PowerShell is required, and the Windows machine/VM that the script
is being run from must be joined to the domain being inspected.

## Usage

```bash
$ ./GetInvalidGroups.ps1
# you should see output corresponding to the request/response sequence, and the invalid
# groups, if any, will be populated in the file "C:\out.csv"
```
