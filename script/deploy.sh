#!/bin/bash

GIT_CMD=$(which git)
GIT_SCHE="https://"
GIT_USER="ryuichi1208"
GIT_MAIL="ryucrosskey@gmail.com"
GIT_REPO="vim-dep-kun"

function git_clone()
{
  ${GIT_CMD} clone ${GIT_SCHE}${GIT_USER}:${GIT_PASS}@github.com/${GIT_USER}/${GIT_REPO}.git
  ls -Rl
  cd ${GIT_REPO}

  ${GIT_CMD} config user.name ${GIT_USER}
  ${GIT_CMD} config user.email ${GIT_MAIL}
}

function git_push()
{
  local _GIT_NEW_TAG=$1

  ${GIT_CMD} add .
  ${GIT_CMD} commit -m "tag new ${_GIT_NEW_TAG}"
  ${GIT_CMD} push
}

function git_tag_push()
{
  local _GIT_NEW_TAG=$1

  ${GIT_CMD} tag -a ${GIT_NEW_TAG} -m "New tag ${GIT_NEW_TAG}"
  ${GIT_CMD} show
  ${GIT_CMD} push origin --tags

}

function main()
{

  # Git関連の初期化
  git_clone

  GIT_OLD_TAG=$(cat tag)
  GIT_NEW_TAG=$(echo "${GIT_OLD_TAG}" | awk '{print $1+0.1}')

  sed -i -e "s/${GIT_OLD_TAG}/${GIT_NEW_TAG}/g" tag

  # GitHubへの通常push
  git_push ${GIT_NEW_TAG}

  # GitHubへのTag漬けを実行
  git_tag_push ${GIT_NEW_TAG}
}

main
