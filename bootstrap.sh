#!/bin/bash

sum=($(md5sum data/swat_2015.zip))

if [[ "$sum" != "1f89a97ed230554ff2e9c0b3963a0a6e" ]]; then
    wget -c "https://www.dropbox.com/s/iap6bx5qmklo1w4/swat_2015.zip?dl=0" -O data/swat_2015.zip
else
    echo "File already downloaded! Skipping download"
fi

cd data
unzip -o swat_2015.zip
rm -rf ._*
