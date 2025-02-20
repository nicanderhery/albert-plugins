#!/bin/bash

# Define the source and destination directories
SOURCE_DIR="$(pwd)"
DEST_DIR="$HOME/.local/share/albert/python"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Loop through each folder in plugins, remove it from the destination directory, and copy the new one
for folder in "$SOURCE_DIR/plugins"/*; do
    folder_name=$(basename "$folder")
    rm -rf "$DEST_DIR/$folder_name"
    cp -r "$folder" "$DEST_DIR/"

    echo "Plugin $folder_name has been copied to $DEST_DIR"
done

echo "Plugins have been copied to $DEST_DIR"