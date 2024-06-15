#!/bin/bash

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Unsupported distribution"
    exit 1
fi

# Source the distribution-specific utility script
case $DISTRO in
    debian|ubuntu)
        ./distro_utils_debian.sh
        ;;
    fedora|centos)
        ./distro_utils_redhat.sh
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

echo "Installation completed successfully."
