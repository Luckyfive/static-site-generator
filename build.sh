#!/bin/bash

# Get the repository name from the git remote URL
REPO_URL=$(git config --get remote.origin.url)
REPO_NAME=$(basename -s .git "$REPO_URL")

# Set the basepath to the repository name for GitHub Pages
BASEPATH="/$REPO_NAME/"

echo "Building site with basepath: $BASEPATH"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Run the static site generator with the basepath
python src/main.py "$BASEPATH"

# Deactivate virtual environment
deactivate

echo "Build complete! The site has been generated in the docs directory."
echo "To deploy to GitHub Pages:"
echo "1. Commit and push the changes"
echo "2. Go to your repository's Settings > Pages"
echo "3. Select 'main' branch and '/docs' folder as the source"
echo "4. Your site will be available at: https://$(dirname "$REPO_URL" | cut -d':' -f2).github.io/$REPO_NAME/"
