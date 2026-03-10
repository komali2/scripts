#!/bin/bash

set -e

# Configuration
DSLR_BASE="/mnt/nas_maindataset/media/Pictures/dlsr"
VIDEO_BASE="/mnt/nas_maindataset/media/Pictures/video"
DATE_FORMAT=$(date +%Y.%m.%d)
LOG_FILE="./sync_error.log"

usage() {
    echo "Usage: $0 {dslr|gopro|360}"
    exit 1
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_FILE"
}

sync_files() {
    local dest_dir="$1"
    local file_pattern="$2"  # empty means all files, otherwise glob pattern

    # Create destination directory
    if ! mkdir -p "$dest_dir"; then
        log_error "Failed to create destination directory: $dest_dir"
        exit 1
    fi

    # Build rsync command
    local rsync_opts=(-av --checksum --progress)

    if [[ -n "$file_pattern" ]]; then
        # Specific file pattern (e.g., *.MP4)
        shopt -s nullglob
        local files=($file_pattern)
        shopt -u nullglob

        if [[ ${#files[@]} -eq 0 ]]; then
            log_error "No files matching pattern '$file_pattern' found in current directory"
            exit 1
        fi

        # rsync specific files
        if ! rsync "${rsync_opts[@]}" "${files[@]}" "$dest_dir/"; then
            log_error "rsync failed for pattern '$file_pattern' to $dest_dir"
            exit 1
        fi

        # Verify files transferred correctly using checksum comparison
        local failed=0
        for src_file in "${files[@]}"; do
            local filename=$(basename "$src_file")
            local dest_file="$dest_dir/$filename"

            if [[ ! -f "$dest_file" ]]; then
                log_error "Verification failed: $filename not found at destination"
                failed=1
            else
                local src_sum=$(md5sum "$src_file" | awk '{print $1}')
                local dest_sum=$(md5sum "$dest_file" | awk '{print $1}')
                if [[ "$src_sum" != "$dest_sum" ]]; then
                    log_error "Verification failed: checksum mismatch for $filename"
                    failed=1
                fi
            fi
        done

        if [[ $failed -eq 1 ]]; then
            log_error "Verification failed - source files NOT removed"
            exit 1
        fi

        # Remove source files on success
        rm -f "${files[@]}"
        echo "Successfully synced ${#files[@]} file(s) to $dest_dir"
        echo "Source files removed."

    else
        # All files in current directory
        shopt -s nullglob
        local files=(./*)
        shopt -u nullglob

        # Filter to only files (not directories)
        local file_list=()
        for f in "${files[@]}"; do
            [[ -f "$f" ]] && file_list+=("$f")
        done

        if [[ ${#file_list[@]} -eq 0 ]]; then
            log_error "No files found in current directory"
            exit 1
        fi

        # rsync all files
        if ! rsync "${rsync_opts[@]}" "${file_list[@]}" "$dest_dir/"; then
            log_error "rsync failed to $dest_dir"
            exit 1
        fi

        # Verify files transferred correctly
        local failed=0
        for src_file in "${file_list[@]}"; do
            local filename=$(basename "$src_file")
            local dest_file="$dest_dir/$filename"

            if [[ ! -f "$dest_file" ]]; then
                log_error "Verification failed: $filename not found at destination"
                failed=1
            else
                local src_sum=$(md5sum "$src_file" | awk '{print $1}')
                local dest_sum=$(md5sum "$dest_file" | awk '{print $1}')
                if [[ "$src_sum" != "$dest_sum" ]]; then
                    log_error "Verification failed: checksum mismatch for $filename"
                    failed=1
                fi
            fi
        done

        if [[ $failed -eq 1 ]]; then
            log_error "Verification failed - source files NOT removed"
            exit 1
        fi

        # Remove source files on success
        rm -f "${file_list[@]}"
        echo "Successfully synced ${#file_list[@]} file(s) to $dest_dir"
        echo "Source files removed."
    fi
}

# Main
if [[ $# -ne 1 ]]; then
    usage
fi

case "$1" in
    dslr)
        DEST_DIR="$DSLR_BASE/$DATE_FORMAT"
        echo "Syncing DSLR files to $DEST_DIR..."
        sync_files "$DEST_DIR" ""
        ;;
    gopro)
        DEST_DIR="$VIDEO_BASE/$DATE_FORMAT"
        echo "Syncing GoPro MP4 files to $DEST_DIR..."
        sync_files "$DEST_DIR" "*.MP4"
        ;;
    360)
        DEST_DIR="$VIDEO_BASE/${DATE_FORMAT}.360"
        echo "Syncing 360 files to $DEST_DIR..."
        sync_files "$DEST_DIR" ""
        ;;
    *)
        usage
        ;;
esac

echo "Done!"
