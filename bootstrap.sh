#!/bin/bash

sum=($(md5sum data/swat_2015.zip))

if [[ "$sum" != "f417d68eeb219e8a02d19a25c08cf262" ]]; then
    wget -c "https://www.dropbox.com/s/iap6bx5qmklo1w4/swat_2015.zip?dl=0" -O data/swat_2015.zip
else
    echo "File already downloaded! Skipping download"
fi

cd data
unzip -o swat_2015.zip
rm -rf ._*
