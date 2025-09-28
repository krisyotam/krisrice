#!/usr/bin/env bash

# --- CONFIGURATION ---
# Define folders as NAME|PATH
FOLDERS=(
  "Wallpapers|$HOME/Pictures/Wallpapers"
  "Anime|$HOME/Pictures/AnimeWalls"
  "Nature|$HOME/Pictures/Nature"
)

# --- FUNCTIONS ---

pick_folder() {
  echo "Select a folder:"
  local i=1
  for entry in "${FOLDERS[@]}"; do
    name="${entry%%|*}"
    echo "$i) $name"
    ((i++))
  done
  read -rp "Choice: " choice
  folder="${FOLDERS[$((choice-1))]}"
  path="${folder#*|}"
  echo "$path"
}

list_files() {
  local dir="$1"
  mapfile -t files < <(find "$dir" -maxdepth 1 -type f | sort)
  local total="${#files[@]}"

  if (( total == 0 )); then
    echo "No files found in $dir"
    exit 1
  fi

  local page=0
  local per_page=10

  while true; do
    clear
    echo "Files in $dir (page $((page+1)))"
    echo "----------------------------------"
    local start=$((page*per_page))
    local end=$((start+per_page))
    (( end > total )) && end=$total

    for ((i=start; i<end; i++)); do
      base="$(basename "${files[$i]}")"
      echo "$((i+1))) $base"
    done

    echo
    echo "n) Next page   p) Previous page   q) Quit"
    read -rp "Select file number: " input

    case "$input" in
      [0-9]*)
        idx=$((input-1))
        if (( idx >= 0 && idx < total )); then
          echo "Running: setbg \"${files[$idx]}\""
          setbg "${files[$idx]}"
          exit 0
        else
          echo "Invalid choice"
        fi
        ;;
      n) (( (page+1)*per_page < total )) && ((page++)) ;;
      p) (( page > 0 )) && ((page--)) ;;
      q) exit 0 ;;
      *) echo "Invalid input" ;;
    esac
  done
}

# --- MAIN ---
folder_path=$(pick_folder)
list_files "$folder_path"
