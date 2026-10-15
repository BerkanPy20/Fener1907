#!/bin/bash

# Check if correct number of arguments provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 source_repo_url destination_repo_url"
    echo "   - source_repo_url: the source git repo"
    echo "   - destination_repo_url: an empty git repo"
    exit 1
fi

SOURCE_REPO=$1
DEST_REPO=$2


kill_history(){
        rm -rf .git

}

init_new_repo(){
    git init
    git add *
    
    git add */.*
    git commit -m "clean commit"
    git branch -M main
}

exchange_origin(){
    git remote remove origin
    git remote add origin "$DEST_REPO"
}

echo "--- clone repo: $SOURCE_REPO ---"

git clone $SOURCE_REPO _workdir

cd _workdir

git filter-branch --force --index-filter \
    'git rm -r --cached --ignore-unmatch "*solution*"' \
    --prune-empty --tag-name-filter cat -- --all

rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now


echo "--- kill history ---"

kill_history

init_new_repo


echo "--- change origin to $DEST_REPO ---"

exchange_origin

echo "--- push to new origin ---"

# Push the cleaned repository to the destination
git push -u origin --all
git push -u origin --tags

echo "Repository forked to $DEST_REPO without files and folders matching '*solution*'."

echo "--- clean _workdir ---"

cd ..
rm -rf _workdir
