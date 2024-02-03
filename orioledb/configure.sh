#!/bin/bash
set -ex

function downloadsource() {
  URL=$1
  LOCALSOURCE=~/rpmbuild/SOURCES/$(basename $URL)
  [ -f "${LOCALSOURCE}" ] && return
  mkdir -p $(dirname ${LOCALSOURCE})
  curl -L "${URL}" -o "${LOCALSOURCE}"
  if ! file "${LOCALSOURCE}" | grep -q gzip; then
    echo "${URL} does not seem like a proper tar file, does the tag exist?"
    rm "${LOCALSOURCE}"
    exit 1
  fi
}

function gen_rpm_macros() {
  GITREPO=$1
  GITSOURCE=$2
  GITTAG=$3
  PGMAJORVERSION=$4

  echo "%pgmajorversion ${PGMAJORVERSION}
  %packageversion ${PGMAJORVERSION}0
  %url ${GITREPO}
  %source0 ${GITSOURCE}
  %gittag ${GITTAG}
  " > ~/.rpmmacros
}

GITORIGIN=${GITORIGIN:-https://github.com/orioledb/orioledb}
if [ -z "${GITTAG}" ]; then
  echo "We need GITTAG to be set to a proper tag in ${GITORIGIN}"
  exit 1
fi
grep -E '^(NAME|VERSION)=' /etc/os-release


GITSOURCE=${GITORIGIN}/archive/${GITTAG}.tar.gz
mkdir -p ~/rpmbuild/SOURCES
touch ~/rpmbuild/SOURCES/setenv
if ! which pg_config; then
  echo "pg_config is not in path, autodetecting it"
  LATEST_PGVERSION=$(ls /usr/pgsql-*/bin/pg_config | tail -n1)
  if [ -z "${LATEST_PGVERSION}" ]; then
    echo "Could not find pg_config. Are postgresqlnn-devel packages properly installed?"
    exit 1
  fi
  PGBIN=$(dirname ${LATEST_PGVERSION})
  echo "export PATH=$PATH:$PGBIN" >> ~/rpmbuild/SOURCES/setenv
  export PATH=$PATH:$PGBIN
fi
if [ "${PGVERSION}" = "" ]; then
  PGVERSION=$(which pg_config | sed -n 's|^/usr/pgsql-||;s|/bin/pg_config$||;/[0-9]\+/p')
fi
if [ ! "${PGVERSION}" -gt 11 ]; then
  echo "Unsupported PostgreSQL release ${PGVERSION}"
fi
gen_rpm_macros "${GITORIGIN}" "${GITSOURCE}" "${GITTAG}" "${PGVERSION}"
downloadsource "${GITSOURCE}"
