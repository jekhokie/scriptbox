#!/bin/sh
#
# Purpose: Builds the respective container images required to run and test the various
#          log4j log4shell exploits contained in this repository.

YELLOW="\033[1;33m"
RED="\033[0;31m"
GREEN="\033[0;32m"
NONE="\033[0m"

containerImages=(
  log4shell-bind9-service
  log4shell-bind9-interface
  log4shell-openldap-service
  log4shell-app-2.8.2-vulnerable
)

for containerImage in "${containerImages[@]}"; do
  echo "${YELLOW}Building ${containerImage} container image...${NONE}"
  cd $containerImage/

  # build the java applications if necessary
  if [[ $containerImage =~ ^log4shell-app-.*$ ]]; then
    mvn package
  fi

  docker build -t $containerImage .
  if [[ $? -eq 0 ]]; then
    echo "${GREEN}SUCCESS: Done!${NONE}"
    cd ../
  else
    echo "${RED}FAIL: Something went wrong building ${containerImage} container image!${NONE}"
    exit 1
  fi
done

echo
echo "${YELLOW}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~${NONE}"
echo "${GREEN}List of container image names:${NONE}"
for containerImage in "${containerImages[@]}"; do
  echo "${GREEN}  - ${containerImage}${NONE}"
done
echo
