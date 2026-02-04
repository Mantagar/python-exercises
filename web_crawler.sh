#!/bin/bash

declare -A crawled_urls

crawl() {
  local url=$1
  local depth=$2
  if [[ -n "${crawled_urls[$url]}" ]]; then return 0; fi
  crawled_urls['$url']=1

  echo "$depth - $url"

  if [[ $depth -le 0 ]]; then return 0; fi
  depth=$((depth - 1))

  html="$(curl $url --silent)"
  for child_url in $(echo $html | grep -oP 'https?://[\w:/.]*'); do
    crawl "$child_url" $depth
  done
  
}

starting_url=$1
starting_depth=$2
crawl "$starting_url" $starting_depth 
