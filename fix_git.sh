#!/bin/bash
git status
git add assets/profile/hero-banner.svg
git add assets/profile/architecture/engineering-matrix.svg
git commit -m "Fix SVGs merge conflict and text wrapping"
git push
echo "Done"