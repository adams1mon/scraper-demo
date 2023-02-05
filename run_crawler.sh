#!/bin/bash

interval_seconds=$1
interval_seconds=${interval_seconds:-60}

echo "running crawler every $interval_seconds seconds"
while true
do
  echo "running crawler"
  scrapy crawl water_interruptions
  sleep $interval_seconds
done