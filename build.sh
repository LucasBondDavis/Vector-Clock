#!/usr/bin/env bash

#rm -rf bin # clean bin
mkdir bin


# copy python files from src to bin
cp -R src/ bin/

cp run.sh bin/

echo Done!

exit 0
