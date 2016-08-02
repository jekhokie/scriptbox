# Purpose: Populate a CSV file with information corresponding to any distribution list that
#          is invalid. A DL is 'invalid' in the scope of this script if one of the following
#          conditions is true:
#
#            1. There is no manager specified for the group.
#            2. The manager of the group is an inactive user.
#            3. Manager specified cannot be resolved through Active Directory.

# where to write the output to
$output_file = "C:\out.csv"

# output start time
$start = Get-Date
Write-Host "Starting script at $($start)..."

# initialize variables
$results = @()
$groups = Get-ADGroup -LDAPFilter "(&(objectCategory=group)(proxyAddresses=*)(mail=*))" -Properties displayname,mail,managedby,whencreated,groupcategory

# go through each group to determine if it's suspect
ForEach ($group in $groups) {
    $add = $false

    Try {
        $group_details = @{
            DisplayName   = $group.DisplayName
            Email         = $group.Mail
            GroupType     = $group.GroupCategory
            Created       = $group.WhenCreated
            Manager       = ""
            Errors        = ""
        }

        If ($group.ManagedBy -eq $null) {
            # no manager specified
            $add = $true
        } ElseIf ($group.ManagedBy -ne $null) {
            Try {
                # attempt to determine if the manager is an active user
                # add the group information if the manager is not active
                $user_enabled = Get-ADUser -Identity $group.ManagedBy | %{$_.enabled}

                # set the specified manager and the fact that the manager is inactive if true
                If ($user_enabled -eq $false) {
                    $add = $true
                    $group_details.Set_Item("Manager", $group.ManagedBy)
                }
            } Catch {
                # issue with identifying the user specified as the manager - need to add this
                $add = $true
                $group_details.Set_Item("Manager", $group.ManagedBy)
                $group_details.Set_Item("Errors", $_.Exception.Message)
            }
        }

        # add group to array if we've found an anomaly
        If ($add -eq $true) {
            $results += [PSCustomObject]$group_details
        }
    } Catch {
        Write-Host "UNRECOVERABLE ERROR: $($_.Exception.Message)"
    }
}

# output the results
$results | Export-Csv -Path $output_file -NoTypeInformation

# output how long this took
$stop = Get-Date
Write-Host "Script complete at $($stop)"
Write-Host "==========================="
Write-Host "TOTAL TIME (seconds): $(($stop - $start).TotalSeconds)"
