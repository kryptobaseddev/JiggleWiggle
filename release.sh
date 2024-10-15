#!/bin/bash

source /venv/Scripts/activate

# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Ensure the script exits on any error
set -e

# Helper function to display usage instructions
usage() {
  echo "Usage: $0 [major|minor|patch]"
  exit 1
}

# Check for input arguments
if [ -z "$1" ]; then
  usage
fi

# Read the current version from version.txt
CURRENT_VERSION=$(cat version.txt)

# Split the version into major, minor, patch
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Bump the version based on the input
if [ "$1" == "major" ]; then
  MAJOR=$((MAJOR + 1))
  MINOR=0
  PATCH=0
elif [ "$1" == "minor" ]; then
  MINOR=$((MINOR + 1))
  PATCH=0
elif [ "$1" == "patch" ]; then
  PATCH=$((PATCH + 1))
else
  usage
fi

# Create the new version number
NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "Bumping version from $CURRENT_VERSION to $NEW_VERSION"

# Write the new version to version.txt
echo "$NEW_VERSION" > version.txt

# Generate the changelog
git-changelog

# Add the updated files
git add version.txt CHANGELOG.md

# Commit the changes
git commit -m "chore(release): bump version to $NEW_VERSION"

# Tag the release with the new version
git tag "v$NEW_VERSION"

# Push the changes and the new tag to the repository
git push origin main --tags

# Compile the app using pyinstaller
echo "Compiling the app..."
pyinstaller --onefile --windowed --icon=assets/icon.ico app.py

# Ensure that the .exe file exists
EXE_FILE="dist/app.exe"
if [ ! -f "$EXE_FILE" ]; then
  echo "Error: Compiled app.exe not found!"
  exit 1
fi

# Upload the .exe to the GitHub release using the GitHub API
echo "Uploading app.exe to the GitHub release..."

# Replace <username>/<repo> with your GitHub username and repository
GITHUB_REPO="kryptobaseddev/JiggleWiggle"

# Create the release with the new version
RELEASE_RESPONSE=$(curl -s -X POST "https://api.github.com/repos/$GITHUB_REPO/releases" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d @- <<EOF
{
  "tag_name": "v$NEW_VERSION",
  "target_commitish": "main",
  "name": "v$NEW_VERSION",
  "body": "Release version $NEW_VERSION",
  "draft": false,
  "prerelease": false
}
EOF
)

# Extract the upload URL for the release asset
UPLOAD_URL=$(echo "$RELEASE_RESPONSE" | jq -r '.upload_url' | sed -e "s/{?name,label}//")

# Upload the .exe file to the release
curl -s --data-binary @"$EXE_FILE" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  "$UPLOAD_URL?name=app-v$NEW_VERSION.exe"

echo "Release $NEW_VERSION has been created and the .exe uploaded."
