#!/bin/bash

GIT_CMD=$(which git)
GIT_SCHE="https://"
GIT_USER="ryuichi1208"
GIT_PASS="Abjlfhy31"
GIT_REPO="vim-dep-kun"

#${GIT_CMD} clone ${GIT_SCHE}${GIT_USER}:${GIT_PASS}@github.com/${GIT_USER}/${GIT_REPO}.git
#ls -Rl

GIT_OLD_TAG=$(cat tag)
GIT_NEW_TAG=$(echo "${GIT_OLD_TAG} + 0.1" | bc)

sed -i -e "s/${GIT_OLD_TAG}/${GIT_NEW_TAG}/g" tag

${GIT_CMD} add .
${GIT_CMD} commit -m "tag new ${GIT_NEW_TAG}"
${GIT_CMD} push