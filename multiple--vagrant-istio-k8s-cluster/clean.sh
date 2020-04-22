#!/bin/bash

TEMP_PATH=shared/kubernetes

echo "This will destroy all contents in the $TEMP_PATH/* directory"
echo "Note that this should *only* be done if you're expecting to create a"
echo "new cluster or have secured the contents for nodes to join your master."

read -p "Are you sure you want to clear the contents? [no/yes]: " CLEANUP
if [[ "$CLEANUP" = "yes" ]]; then
  echo "  deleting contents of $TEMP_PATH/*..."
  find $TEMP_PATH/* -not -path ".gitignore" -exec rm -f {} \;
  echo "  contents cleared!"
fi
