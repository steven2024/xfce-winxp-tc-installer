import subprocess
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class WinXPThemeInstaller:
    def __init__(self):
        # Create a new window
        self.window = Gtk.Window()
        self.window.set_title("Windows XP Theme Installer")
        self.window.set_default_size(400, 300)
        self.window.connect("destroy", Gtk.main_quit)

        # Create a vertical box to hold everything
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window.add(vbox)

        # Install WinXP Theme button
        install_button = Gtk.Button(label="Install WinXP Theme")
        install_button.connect("clicked", self.install_winxp_theme)
        vbox.pack_start(install_button, expand=True, fill=True, padding=10)

        # Install WelcomeXP Theme checkbox
        self.install_welcomexp = Gtk.CheckButton(label="Install WelcomeXP Theme")
        vbox.pack_start(self.install_welcomexp, expand=True, fill=True, padding=10)

        # Status label
        self.status_label = Gtk.Label()
        vbox.pack_start(self.status_label, expand=False, fill=True, padding=10)

        # Set the current working directory to the parent folder of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        # Show all elements
        self.window.show_all()

    def install_winxp_theme(self, widget):
        try:
            # Step 1: Detect Linux distribution
            distro_info = self.detect_linux_distribution()
            if distro_info is None:
                raise RuntimeError("Unsupported Linux distribution.")

            # Step 2: Install build-time dependencies
            self.update_status("Installing build-time dependencies...")
            self.install_dependencies(distro_info)

            # Step 3: Clone the repository and build the project
            self.update_status("Cloning and building the WinXP Theme project...")
            subprocess.run(['git', 'clone', 'https://github.com/rozniak/xfce-winxp-tc.git'])
            subprocess.run(['bash', '-c', 'cd xfce-winxp-tc/packaging && ./buildall.sh'])

            # Step 4: Install the output packages
            self.update_status("Installing WinXP Theme packages...")
            self.install_packages()

            self.update_status("WinXP Theme installed successfully!")
        except Exception as e:
            self.update_status(f"Error installing WinXP Theme: {str(e)}")

        # Check if WelcomeXP installation is requested
        if self.install_welcomexp.get_active():
            self.install_welcomexp_theme(distro_info)

    def install_welcomexp_theme(self, distro_info):
        try:
            # Step 5: Clone and install nody-greeter
            self.update_status("Installing nody-greeter...")
            subprocess.run(['git', 'clone', '--recursive', 'https://github.com/JezerM/nody-greeter.git'])
            subprocess.run(['bash', '-c', 'cd nody-greeter && git checkout 1.5.2'])
            subprocess.run(['bash', '-c', 'cd nody-greeter && npm install'])
            subprocess.run(['bash', '-c', 'cd nody-greeter && npm run rebuild'])
            subprocess.run(['bash', '-c', 'cd nody-greeter && npm run build'])
            subprocess.run(['sudo', 'node', 'make', 'install'])

            # Step 6: Clone and install WelcomeXP
            self.update_status("Installing WelcomeXP Theme...")
            subprocess.run(['git', 'clone', 'https://github.com/mshernandez5/WelcomeXP.git'])
            subprocess.run(['bash', '-c', 'cd WelcomeXP && git checkout v0.4.1'])

            xp_fonts_dir = 'winxp-fonts'  # Assuming this is the directory structure after cloning

            # Step 8: Copy XP fonts to WelcomeXP/fonts/
            self.update_status("Copying XP fonts to WelcomeXP...")
            subprocess.run(['sudo', 'mkdir', '-p', '/usr/share/web-greeter/themes/WelcomeXP/fonts'])
            subprocess.run(['sudo', 'cp', f'{xp_fonts_dir}/tahoma.ttf', '/usr/share/web-greeter/themes/WelcomeXP/fonts'])
            subprocess.run(['sudo', 'cp', f'{xp_fonts_dir}/tahomabd.ttf', '/usr/share/web-greeter/themes/WelcomeXP/fonts'])
            subprocess.run(['sudo', 'cp', f'{xp_fonts_dir}/FRADMIT.TTF', '/usr/share/web-greeter/themes/WelcomeXP/fonts'])
            subprocess.run(['sudo', 'chmod', '-R', '755', '/usr/share/web-greeter/themes/WelcomeXP/fonts'])

            # Step 9: Configure lightdm for WelcomeXP
            self.update_status("Configuring lightdm for WelcomeXP...")
            self.configure_lightdm(distro_info)

            self.update_status("WelcomeXP Theme installed successfully!")
        except Exception as e:
            self.update_status(f"Error installing WelcomeXP Theme: {str(e)}")

    def detect_linux_distribution(self):
        try:
            # Read /etc/os-release to detect distribution
            distro_id = ""
            version_id = ""
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('ID='):
                        distro_id = line.split('=')[1].strip().strip('"')
                    elif line.startswith('VERSION_ID='):
                        version_id = line.split('=')[1].strip().strip('"')

            return {'ID': distro_id, 'VERSION_ID': version_id}
        except Exception as e:
            print(f"Error detecting Linux distribution: {str(e)}")
            return None

    def install_dependencies(self, distro_info):
        try:
            if distro_info['ID'].lower() == 'debian':
                subprocess.run(['sudo', 'apt', 'install', 'libgdk-pixbuf-2.0-dev', 'libglib2.0-dev', 'libgtk-3-dev', 'liblightdm-gobject-1-dev', 'gettext', 'libsqlite3-dev', 'python3-packaging', 'python3-venv', 'ruby-sass', 'libgarcon-1-dev', 'libgarcon-gtk3-1-dev', 'libpulse-dev', '-y'])
            elif distro_info['ID'].lower() == 'alpine':
                subprocess.run(['sudo', 'apk', 'add', 'libgdk-pixbuf-2.0-dev', 'libglib2.0-dev', 'libgtk-3-dev', 'liblightdm-gobject-1', 'gettext', 'libsqlite3-dev', 'python3-packaging', 'python3-venv', 'ruby-sass', 'libgarcon-1-dev', 'libgarcon-gtk3-1-dev', 'libpulse-dev'])
            elif distro_info['ID'].lower() == 'void':
                subprocess.run(['sudo', 'xbps-install', '-S', 'libgdk-pixbuf-2.0-dev', 'libglib2.0-dev', 'libgtk-3-dev', 'liblightdm-gobject-1', 'gettext', 'libsqlite3-dev', 'python3-packaging', 'python3-venv', 'ruby-sass', 'libgarcon-1-dev', 'libgarcon-gtk3-1-dev', 'libpulse-dev'])
            else:
                raise RuntimeError(f"Unsupported distribution: {distro_info['ID']}")
        except Exception as e:
            raise RuntimeError(f"Error installing dependencies: {str(e)}")

    def configure_lightdm(self, distro_info):
        try:
            if distro_info['ID'].lower() in ['debian', 'alpine', 'void']:
                # Modify /etc/lightdm/web-greeter.yml and set theme: WelcomeXP
                subprocess.run(['sudo', 'sed', '-i', '/theme:/c\    theme: WelcomeXP', '/etc/lightdm/web-greeter.yml'])
            else:
                raise RuntimeError(f"Unsupported distribution: {distro_info['ID']}")
        except Exception as e:
            raise RuntimeError(f"Error configuring lightdm: {str(e)}")

    def update_status(self, message):
        # Update the status label
        self.status_label.set_text(message)
        while Gtk.events_pending():
            Gtk.main_iteration()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script needs to be run with superuser privileges (sudo).")
        exit(1)

    WinXPThemeInstaller()
    Gtk.main()
