#!/bin/bash

_ruby()
{
  local cur prev filename
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  filename=""

  # tab-complete test names once the -n switch is detected
  if [[ ${prev} == '-n' ]] ; then
    # parse the command line arguments and find the name of the file
    for w in "${COMP_WORDS[@]}" ; do
      if [[ ${w} =~ .*\.rb ]] ; then
        filename=${w}
        break
      fi
    done

    if [[ -f ${filename} ]] ; then
      local tests=$(for x in `grep "test \".*\"" ${filename} | awk -F'"' '{print $1 $2}' | sed -e 's/^ *//' | sed -E 's/ +/_/g'`; do echo ${x} ; done )
      COMPREPLY=( $(compgen -W "${tests}" -- ${cur}) )
      return 0
    fi
  fi

  # default to file completion for any other instances besides the test selector switch
  _filedir
}
complete -F _ruby ruby
