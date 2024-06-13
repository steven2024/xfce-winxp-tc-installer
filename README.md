###  This is a PyGTK-based GUI program to automate the installation process of the winxp-xfce-tc and WelcomeXP themes on Linux systems. This aims to simplify the installation steps involved, which currently require manual compilation and package installation.

**Current Progress**

The current UI of the PyGTK program is simple and user-friendly. It features a main window titled "Windows XP Theme Installer" with a straightforward layout. You can click a button to install the winxp-xfce-tc theme and optionally check a box to install the WelcomeXP theme. Below these controls, a status label provides real-time updates on the installation process, keeping you informed of progress and any issues that arise. Overall, the design focuses on ease of use, guiding you through the installation process with clear, concise interactions.

_Currently, the user interface (UI) for the installation wizard doesn't resemble Windows XP at all. However, once I streamline the auto-installation process, I plan to overhaul the UI to be accurate to the Windows XP OOBE. This will include redesigning the overall layout to closely mirror the classic Windows XP installation experience._

The PyGTK program is designed to:

    Install winxp-xfce-tc Theme: Automate the installation of the theme by handling dependencies, compiling necessary components, and installing required packages using package manager commands appropriate for the user's Linux distribution.
    Option to Install WelcomeXP: Provide an option to install WelcomeXP (https://github.com/mshernandez5/WelcomeXP) alongside winxp-xfce-tc, which mimics the Windows XP login screen.

**Future Plans**

Once the auto-installation process for winxp-xfce-tc is streamlined:

    Recreating WinXP OOBE: Recreation of the Windows XP Out-of-Box Experience (OOBE) within the winxp-xfce-tc environment. This includes developing an interface that mimics the setup process of Windows XP, providing users with a simplified installation experience. (as mentioned in Issue #81)
    Enhancing User Interaction: Implement features such as graphical and text-mode setup options (as mentioned in Issue #81) based on the user's system configuration, ensuring compatibility and ease of use across different Linux distributions and setups.

**Next Steps**

    Refine the PyGTK program to ensure smooth installation of winxp-xfce-tc and WelcomeXP themes.
    Make the XP OOBE as accurate as possible.
    Test and iterate on the installation process to handle edge cases and improve user experience.
    Gather feedback and suggestions for further enhancements and features.
    
**Features**

    Install WinXP Theme (xfce-winxp-tc):
        Clones and builds the WinXP Theme project from GitHub (https://github.com/rozniak/xfce-winxp-tc.git).
        Installs necessary build dependencies specific to supported Linux distributions.
        Configures system settings to integrate the WinXP-like theme.

    Install WelcomeXP Theme:
        Clones and installs WelcomeXP theme components from GitHub (https://github.com/mshernandez5/WelcomeXP.git).
        Sets up necessary fonts and configurations for the WelcomeXP theme.

Requirements:

    Operating System Compatibility:
        Supports Linux distributions with specific package management tools (apt, apk, xbps) depending on the detected distribution.

Prerequisites:

    Superuser Privileges:
        Ensure the script is executed with superuser privileges (sudo) to perform system-wide installations and configurations.
    Run Setup and Installation:
        Execute installer.sh to set up dependencies and then installer.py to install themes.

Usage:

    Clone the Repository:

    bash git clone https://github.com/steven2024/xfce-winxp-tc-installer.git
    cd xfce-winxp-tc-installer

Run the Setup and Installation Script:

    sudo ./installer.sh

    Installation Steps:
        Click "Install WinXP Theme" to initiate the installation of xfce-winxp-tc.
        Optionally select "Install WelcomeXP Theme" to install WelcomeXP.
        Follow on-screen prompts and status updates in the graphical interface for installation progress.

    Completion:
        Upon successful installation, the WinXP-like theme should be integrated into your Linux desktop environment.

Notes:

    Ensure internet connectivity and repository access for package installation.
    Customize configurations or additional steps based on specific Linux distributions not covered by default.

xfce-winxp-tc by Rory Fewell (rozniak):
 Windows XP Total Conversion for XFCE.
WelcomeXP by Markus Hernandez (mshernandez5):
 A nody-greeter theme to mimic the Windows XP login screen.
