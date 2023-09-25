#!/bin/bash

#this script will nuke docs/ and rebuild it with an index of `find -iname *.md` as a root wiki liked page and all other .md files as subpages

rm -fr docs
mkdir docs
touch docs/index.md
echo "# Index of all .md files in this repo" >> docs/index.md
echo "" >> docs/index.md

#the files have spaces in the names

files=()
while IFS=  read -r -d $'\0'; do
    files+=("$REPLY")
done < <(find . -iname '*.md' -print0)

#perform mkdir on all the files to create the directory structure
for file in "${files[@]}"; do
    #echo "$file"
    #echo "${file%/*}"
    mkdir -p docs/"${file%/*}"
done

#copy all the files to the docs directory
for file in "${files[@]}"; do
    cp "$file" docs/"$file"
done

#now we need to create the index.md file

#first we need to remove the ./ from the front of the files
for file in "${files[@]}"; do
    #echo "$file"
    #echo "${file%/*}"
    file="${file#./}"
    #echo "$file"
    #echo "${file%/*}"
    file="${file%.*}"
    #echo "$file"
    #echo "${file%/*}"
    file="${file//\// }"
    #echo "$file"
    #echo "${file%/*}"
    echo "* [$file]($file)" >> docs/index.md
done

