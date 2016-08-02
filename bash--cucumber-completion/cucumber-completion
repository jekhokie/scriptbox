#!/bin/bash

_cucumber()
{
  local cur prev filename
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  filename=""

  # tab-complete test names once a colon is detected following a feature file name
  if [[ ${prev} =~ .*\.feature && ${cur} =~ : ]] ; then
    # parse the command line arguments and find the name of the file
    for w in "${COMP_WORDS[@]}" ; do
      if [[ ${w} =~ .*\.feature ]] ; then
        filename=${w}
        break
      fi
    done

    if [[ -f ${filename} ]] ; then
      local old_ifs tests line_numbers current_lookup

      # set the field input separator to a comma and get tests
      old_ifs=$IFS
      IFS=","
      tests=( $(for x in `grep -n "Scenario:.*" ${filename} | awk -F':' '{printf "%5s  %s,", $1, $3}' ` ; do echo ${x} ; done ) )

      # iterate over array and grab all possible line numbers as options
      for x in ${tests[@]}; do
        line_numbers=("${line_numbers[@]}" `grep -o [0-9]* <<<$x`)
      done

      # reset the input field separator to its original value
      IFS=$old_ifs

      # output the results of line numbers and corresponding tests
      echo
      echo
      cat <<EOT
   LN   TEST
-----   -----------------------------------
$tests

POSSIBLE LINE NUMBERS:
EOT

      COMPREPLY=($(compgen -W "${line_numbers[*]}" -- ""))
      return 0
    fi
  fi

  # default to file completion for any other instances besides the cucumber test selector
  _filedir
}
complete -o nospace -F _cucumber cucumber
