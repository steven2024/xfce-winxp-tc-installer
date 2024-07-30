# Windows XP Theme Installer
**Overview**

This PyGObject-based GUI program automates the installation process of the [xfce-winxp-tc](https://github.com/rozniak/xfce-winxp-tc) theme on Linux systems. It simplifies the installation steps that currently require manual compilation and package installation.

**Current Progress**

The current UI of the PyGObject program is simple and user-friendly. It recreates the Windows XP OOBE. You can click a button to install the winxp-xfce-tc theme.

- ***Note***
    - The installation functionality has been added, but it is currently only available for Debian-based systems. Support for other distributions is planned for future releases.
    - Rozniak has started working on porting my work on the theme installer over to C for integration with his theme. This work is still in progress, and the C-based version is not yet complete. The goal is to enhance the theme installer to be more closely integrated with the theme itself.

**Current Features**

**Recreating WinXP OOBE**

    The program recreates the Windows XP Out-of-Box Experience (OOBE), providing users with a simplified setup experience.
    This includes a user interface that mimics the setup process of Windows XP, complete with visuals and interactions designed to replicate the classic experience.
    It includes the iconic Windows XP intro video and title.wmv.

**Planned Features**

Install WinXP Theme (xfce-winxp-tc)

    Clone and build the WinXP Theme project from GitHub.
    Install necessary build dependencies specific to supported Linux distributions.
    Configure system settings to integrate the WinXP-like theme.

**Future Enhancements**

Enhancing User Interaction

    Graphical and Text-Mode Setup Options:
    Implement features that allow users to choose between graphical and text-mode setup options based on their system configuration. This will improve the user experience by providing a more intuitive interface for those who prefer graphical setups, while also catering to users who are more comfortable with text-based interfaces.

**SKU Selection Dropdown**

SKU Options:

    The installer will feature a SKU selection dropdown to support a range of Windows versions. Currently, users can select from the following SKUs:
        Windows XP Professional
        Windows Server 2003 Standard Edition
        Windows Home Server

This dropdown will provide flexibility for users, allowing them to choose the appropriate Windows version for their specific needs without being restricted to a single SKU.

**LightDM Greeter**

    Welcome Screen and Classic Logon:
    There is a LightDM greeter in xfce-winxp-tc that implements both the Welcome screen and Classic logon functionalities. This greeter is located under /base/logonui. In future updates, the installer might include this LightDM greeter as an option, allowing users to enable or disable the Welcome screen and Classic logon during the installation process.

By implementing these enhancements, I aim to provide a more versatile and user-friendly tool that meets the diverse needs of users.

**Requirements**

- Operating System Compatibility

    Supports Linux distributions with specific package management tools (apt, apk, xbps) depending on the detected distribution.

- Prerequisites

    Superuser Privileges: Ensure the script is executed with superuser privileges (sudo) to perform system-wide installations and configurations.

**Usage**

- Clone the Repository

    ```git clone https://github.com/steven2024/xfce-winxp-tc-installer.git```

    ```cd xfce-winxp-tc-installer```

- Run the Setup and Installation Script

    ```sudo ./installer.sh```

**Installation Steps**

    Click "Install WinXP Theme" to initiate the installation of xfce-winxp-tc.
    Follow on-screen prompts and status updates in the graphical interface for installation progress.

**Completion**

    Upon successful installation, the WinXP-like theme should be integrated into your Linux desktop environment.

- ***Notes***

   - Ensure internet connectivity and repository access for package installation.
   - Customize configurations or additional steps based on specific Linux distributions not covered by default.

## Credits

[xfce-winxp-tc](https://github.com/rozniak/xfce-winxp-tc) by Rory Fewell [(rozniak)](https://github.com/rozniak): Windows XP Total Conversion for XFCE.

