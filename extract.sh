#!/bin/bash

mkdir -p pst_files
mkdir -p output_emails

for dir in output_emails/*; do
    if [ -d "$dir" ]; then
        echo "removing $dir ..."
        rm -rf $dir
    fi
done

for k in pst_files/*.pst; do
    file_name="$(basename $k)"
    dir_name="${file_name%.pst}"
    mkdir -p output_emails/"$dir_name"
    echo "extracting $file_name ..."
    readpst -D -o output_emails/$dir_name pst_files/$file_name
done

python3 mbox_to_eml.py
