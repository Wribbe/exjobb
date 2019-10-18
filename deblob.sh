#!/bin/sh

gpg -d blobby.tar.gz.gpg > blobby.tar.gz
tar -xf blobby.tar.gz
rm -rf blobby.tar.gz
