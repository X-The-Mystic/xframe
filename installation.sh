#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Metasploit Framework
echo "Installing Metasploit Framework..."
sudo apt install -y metasploit-framework

# Additional instructions or installations can be added here
echo "Installation complete! Please ensure to configure Metasploit as needed."