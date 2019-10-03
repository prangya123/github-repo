#!/bin/bash

# Commit Hash Abbreviated
gitHashAbb=$(git log -n 1 --pretty=format:%h)
if [ ! -v gitHashAbb ]; then
  echo "Couldn't fetch value for gitHashAbb"
  exit 1
fi

# Author Name :
gitAuthor=$(git log -n 1 --pretty=format:%an ${gitHashAbb})
if [ ! -v gitAuthor ]; then
  echo "Couldn't fetch value for gitAuthor"
  exit 1
fi

# Branch:
gitBranch=$(git rev-parse --abbrev-ref HEAD)
if [ ! -v gitBranch ]; then
  echo "Couldn't fetch the value for gitBranch"
  exit 1
fi

# Commit Changeset
# running sed helps to get rid of empty blank lines
gitChangeset=$(git log -m -1 --name-status --pretty="format:" ${gitHashAbb} | sed -r '/^\s*$/d' | sort  | uniq)
if [ ! -v gitChangeset ]; then
  echo "Couldn't fetch value for gitChangeset"
  exit 1
fi

# Running 'git config --get ...' to fetch the remote
# url returns the url, but with GHE service account
# info exposed in the URL. Not so nice to see!
gitRepoUrl="https://${REPO_URL}"

savedFile="${WORKSPACE}/${REPO_NAME}_commit_info.txt"
if [ -f "${savedFile}" ]; then
  rm ${savedFile}
fi

echo -e "Hash      : ${gitHashAbb}" > ${savedFile}
echo -e "Author    : ${gitAuthor}" >> ${savedFile}
echo -e "Repo      : ${gitRepoUrl}" >> ${savedFile}
echo -e "Branch    : ${gitBranch}" >> ${savedFile}
echo -e "Changeset :" >> ${savedFile}
echo -e "${gitChangeset}" >> ${savedFile}

echo -e "\nSaved git information to the file ${savedFile}"
