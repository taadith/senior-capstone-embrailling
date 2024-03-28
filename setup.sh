#!/bin/bash

# Install npm packages
tput setaf 2; echo "Installing npm packages...$(tput sgr0)"
npm install

# Install Python packages from requirements.txt
tput setaf 2; echo "Installing Python packages...$(tput sgr0)"
sudo pip install -r src/components/requirements.txt

# Update package lists for upgrades and new package installations
tput setaf 2; echo "Updating package lists...$(tput sgr0)"
sudo apt-get update

# Install TeX Live and XeTeX packages
tput setaf 2; echo "Installing TeX Live and XeTeX packages...$(tput sgr0)"
sudo apt-get install -y texlive texlive-xetex
