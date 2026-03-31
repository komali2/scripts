#!/bin/bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <sd-card-mount-path>"
    echo "Example: $0 /run/media/caleb/10E9-8D4B"
    exit 1
fi

SDCARD="$1"
MUSIC_DIR="$SDCARD/Music"

# Safety checks to prevent accidental deletion of important directories
if [[ ! -d "$SDCARD" ]]; then
    echo "Error: SD card path does not exist: $SDCARD"
    exit 1
fi

# Must be a mount point (not just any directory)
if ! mountpoint -q "$SDCARD"; then
    echo "Error: $SDCARD is not a mount point"
    echo "This script only operates on mounted removable media"
    exit 1
fi

# Must be under /run/media, /media, or /mnt (standard removable media locations)
if [[ ! "$SDCARD" =~ ^/(run/media|media|mnt)/ ]]; then
    echo "Error: $SDCARD is not in a standard removable media location"
    echo "Expected path under /run/media/, /media/, or /mnt/"
    exit 1
fi

# Create Music directory if it doesn't exist
mkdir -p "$MUSIC_DIR"

echo "=== Clearing Music directory (preserving Favorites) ==="
find "$MUSIC_DIR" -mindepth 1 -maxdepth 1 ! -name 'Favorites' -exec rm -rf {} +

echo "=== Getting album list from beet ==="
# Get all albums sorted by added date (most recent first)
mapfile -t ALL_SORTED < <(beet ls -a -f '$id $added' | sort -t' ' -k2,3 -r | awk '{print $1}')

# Split into recent (first 10) and rest (shuffled)
RECENT_IDS=("${ALL_SORTED[@]:0:10}")
REST_IDS=("${ALL_SORTED[@]:10}")

# Shuffle the rest
mapfile -t RANDOM_IDS < <(printf '%s\n' "${REST_IDS[@]}" | shuf)

echo "=== Copying 10 most recent albums ==="
for id in "${RECENT_IDS[@]}"; do
    album_name=$(beet ls -a -f '$album' "album_id:$id")
    echo "Copying: $album_name"
    if ! beet move -cae -d "$MUSIC_DIR" "album_id:$id"; then
        echo "Error copying album, SD card may be full"
        exit 0
    fi
done

echo "=== Filling SD card with random albums ==="
for id in "${RANDOM_IDS[@]}"; do
    album_name=$(beet ls -a -f '$album' "album_id:$id")
    echo "Copying: $album_name"
    if ! beet move -cae -d "$MUSIC_DIR" "album_id:$id"; then
        echo "SD card full, stopping"
        exit 0
    fi
done

echo "=== Done! All albums copied ==="
