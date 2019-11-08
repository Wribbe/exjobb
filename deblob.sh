#!/bin/sh

DIR=blobby
FILE_TAR=${DIR}.tar.gz
FILE_CRYPT=${FILE_TAR}.gpg

if [ "$1" = "--blob" ] && [ -d ${DIR} ]; then
  [ ! -f ${FILE_CRYPT} ] || rm -rf ${FILE_CRYPT}
  tar -czf ${FILE_TAR} ${DIR}
  gpg -c ${FILE_TAR}
else
  gpg -d ${FILE_CRYPT} > ${FILE_TAR}
  tar -xf ${FILE_TAR}
fi
[ ! -f ${FILE_TAR} ] || rm -rf ${FILE_TAR}
