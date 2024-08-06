#!/bin/bash

# Debian specific installation steps here
echo "Running Debian-specific installation utilities..."

# Function to get the absolute path of the script
get_script_path() {
    echo "$(cd "$(dirname "$0")" && pwd)"
}

# Function to check and install build-time dependencies
install_dependencies() {
    echo "Installing build-time dependencies..."
    sudo apt-get install -y libgdk-pixbuf-2.0-dev libglib2.0-dev libgtk-3-dev liblightdm-gobject-1-dev gettext libsqlite3-dev python3-packaging python3-venv ruby-sass libgarcon-1-dev libgarcon-gtk3-1-dev libpulse-dev
}

# Function to clean up old builds
cleanup_old_builds() {
    echo "Cleaning up old builds..."
    SCRIPT_PATH=$(get_script_path)
    rm -rf "$SCRIPT_PATH/xfce-winxp-tc/packaging/xptc/*"
}

# Function to clone and build the WinXP Theme project
build_winxp_theme() {
    echo "Cloning and building the WinXP Theme project..."
    git clone https://github.com/rozniak/xfce-winxp-tc.git
    cd xfce-winxp-tc/packaging || exit 1

    # Build the project
    ./buildall.sh || {
        echo "Build failed. Exiting."
        exit 1
    }

    cd ../..
}

# Function to find the latest build directory
find_latest_build_dir() {
    SCRIPT_PATH=$(get_script_path)
    echo "$(find "$SCRIPT_PATH/xfce-winxp-tc/packaging/xptc" -maxdepth 1 -type d -name 'bbe17d1.master(root).*' -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2)"
}

# Function to install the output packages in a specific order
install_winxp_theme() {
    SCRIPT_PATH=$(get_script_path)
    LATEST_BUILD_DIR=$(find_latest_build_dir)
    
    if [ -z "$LATEST_BUILD_DIR" ]; then
        echo "Latest build directory not found. Exiting."
        exit 1
    fi

    echo "Installing WinXP Theme packages from $LATEST_BUILD_DIR/deb/std/x86_64/fre/..."

    # Find and install the most recent root dependency first
    ROOT_PACKAGE=$(find "$LATEST_BUILD_DIR/deb/std/x86_64/fre" -name "libwintc-comgtk*.deb" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2)
    if [ -n "$ROOT_PACKAGE" ]; then
        sudo dpkg -i "$ROOT_PACKAGE" || {
            echo "Error installing root package $ROOT_PACKAGE. Please check if the package exists."
            exit 1
        }
    else
        echo "Root package libwintc-comgtk not found. Exiting."
        exit 1
    fi

    # Install the other packages
    OTHER_PACKAGES=$(find "$LATEST_BUILD_DIR/deb/std/x86_64/fre" -name "*.deb" ! -name "libwintc-comgtk*.deb" -printf "%T@ %p\n" | sort -n | cut -d' ' -f2)
    for PACKAGE in $OTHER_PACKAGES; do
        sudo dpkg -i "$PACKAGE" || {
            echo "Error installing $PACKAGE. Please check if the package exists."
            exit 1
        }
    done
}

# Install dependencies
install_dependencies

# Clean up old builds
cleanup_old_builds

# Build and install themes
build_winxp_theme
install_winxp_theme

echo "Debian-specific installation completed."
