#!/bin/bash

interval_seconds=$1
interval_seconds=${interval_seconds:-60}

scrapy_path="undefined"
scrapy_shared="/usr/local/bin/scrapy"
scrapy_own="$HOME/.local/bin/scrapy"

if [ -e $scrapy_shared ]
then
  scrapy_path=$scrapy_shared
elif [ -e $scrapy_own ]
then
  scrapy_path=$scrapy_own
else
  echo "could not find scrapy, exiting..."
  exit 1
fi

echo "running crawler every $interval_seconds seconds"
while true
do
  echo "running crawler"
  $scrapy_path crawl water_interruptions
  sleep $interval_seconds
done