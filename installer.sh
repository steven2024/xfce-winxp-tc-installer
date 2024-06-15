#!/bin/bash

# Change directory to the script's location
cd "$(dirname "$0")"

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python
install_python() {
    echo "Installing Python..."
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install python3 -y
    elif command_exists apk; then
        sudo apk update
        sudo apk add python3
    elif command_exists xbps-install; then
        sudo xbps-install -S python3
    else
        echo "Unsupported distribution. Python installation failed."
        exit 1
    fi
}

# Function to install PyGTK
install_pygtk() {
    echo "Installing PyGTK..."
    if command_exists apt-get; then
        sudo apt-get install python3-gi gir1.2-gtk-3.0 -y
    elif command_exists apk; then
        sudo apk add py3-gobject3 py3-gtk3
    elif command_exists xbps-install; then
        sudo xbps-install -S py3-gobject3 py3-gtk3
    else
        echo "Unsupported distribution. PyGTK installation failed."
        exit 1
    fi
}

# Check Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Cannot determine Linux distribution."
    exit 1
fi

# Check if Python is installed
if ! command_exists python3; then
    install_python
fi

# Check if PyGTK is installed
if ! python3 -c 'import gi; gi.require_version("Gtk", "3.0")' 2>/dev/null; then
    install_pygtk
fi

# Run xp.py
echo "Running xp.py..."
python3 "$(dirname "$0")/installer-utils/xp.py"

# Clean up cloned repositories
echo "Cleaning up cloned repositories..."
rm -rf "$(dirname "$0")/xfce-winxp-tc"
rm -rf "$(dirname "$0")/nody-greeter"
rm -rf "$(dirname "$0")/WelcomeXP"
echo "Cleanup completed."
