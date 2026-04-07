#!/bin/sh
# Define the icon names (the middle part of the URL)
icons="backward-fast forward-fast play backward forward plus-minus backward-step forward-step plus circle gear spinner minus stop eject music user equals pause"

for icon in $icons; do
  echo "Downloading $icon..."
  curl -O "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/svgs/solid/${icon}.svg"
done