#!/bin/bash

# Step 1: Checkout main branch
git checkout main
git pull origin main

# Step 2: Generate index.md
echo "# Wiki Index" > index.md
echo "" >> index.md
find . -iname "*.md" | sed -e 's/^\.\///' -e 's/\(.*\)\.md/- [\1](\1\.md)/' >> index.md

# Step 3: Commit changes to main
git add index.md
git commit -m "Automatically generated index.md"
git push origin main

# Step 4: Checkout docs branch and clean
git checkout docs
git rm -r *

# Step 5: Copy contents from main
git checkout main -- .
git add .
git commit -m "Updated docs branch with main branch contents"

# Step 6: Push changes to GitHub
git push origin docs
