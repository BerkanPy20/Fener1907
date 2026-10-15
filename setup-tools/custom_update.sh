#!/bin/bash

# Check if correct number of arguments provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 source_repo_url destination_repo_url"
    echo "Updates an exsiting repo that was initialized with 'custom_clone.sh'"
    exit 1
fi

SOURCE_REPO=$1
DEST_REPO=$2

git clone $SOURCE_REPO _workdir_origin 
git clone $DEST_REPO _workdir_dest 

cd _workdir_origin

git filter-branch --force --index-filter \
    'git rm -r --cached --ignore-unmatch "*solution*"' \
    --prune-empty --tag-name-filter cat -- --all

rm -rf .git


cd ..

cp -r _workdir_origin/* _workdir_dest

cd _workdir_dest

git add *

git add */.*
git commit -m "update"
git push







