import gi
import os
import tempfile
import threading
import subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gst, GstVideo

# Set XDG_RUNTIME_DIR if not set
if 'XDG_RUNTIME_DIR' not in os.environ:
    os.environ['XDG_RUNTIME_DIR'] = tempfile.mkdtemp()

class XPWelcomeWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="XP OOBE Theme Installer")
        self.set_default_size(782, 495)
        self.set_resizable(False)  # Lock the window size

        # Connect to the 'realize' signal to set the custom cursor
        self.connect("realize", self.on_window_realized)

        # Apply GTK theme
        self.apply_gtk_theme('winxp-theme/Windows XP style (Blue)/gtk-3.0/gtk.css')

        # Create a fixed container to hold the background image and overlay elements
        self.fixed_container = Gtk.Fixed()
        self.add(self.fixed_container)

        # Load initial background image (Bitmap20142.jpg)
        self.current_background = 'winxp-imgs/Bitmap20142.jpg'
        self.load_background_image(self.current_background)

        # Create and place text elements
        self.create_text_elements()

        # Create an EventBox to hold the clickable image button
        self.next_button_image = Gtk.Image()
        self.next_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file('winxp-imgs/continue.png')
        self.next_button_pixbuf = self.next_button_pixbuf.scale_simple(30, 30, GdkPixbuf.InterpType.BILINEAR)
        self.next_button_image.set_from_pixbuf(self.next_button_pixbuf)

        self.event_box = Gtk.EventBox()
        self.event_box.set_size_request(30, 30)
        self.event_box.add(self.next_button_image)

        # Create a label with underlined 'N' and white text
        self.next_label = Gtk.Label()
        self.next_label.set_markup('<span foreground="white" font="Tahoma 10"><u>N</u>ext</span>')
        self.next_label.set_halign(Gtk.Align.START)

        # Create a box to hold the label and the button
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.hbox.pack_start(self.next_label, False, False, 0)
        self.hbox.pack_start(self.event_box, False, False, 0)

        # Calculate position for the hbox to be centered at the bottom right corner
        button_x = 782 - 30 - 5  # 782 is the width of the window, 30 is the width of the button, 5 is the amount to move left
        button_y = 495 - 40 + (40 - 30) // 2  # 495 is the height of the window, 40 is the bottom border height

        # Place the hbox at the calculated coordinates on the fixed container
        self.fixed_container.put(self.hbox, button_x - 60, button_y)  # Adjust x position to accommodate the label

        # Connect a signal to handle button clicks
        self.event_box.connect("button-press-event", self.on_next_button_clicked)

        # Video player setup
        self.video_uri = 'intro-wmv/intro-scaled.mp4'  # Path to your video file
        self.init_video_player()

        # Music player setup
        self.init_music_player('title-wma/Isk3k3.mp3')  # Path to your music file

        # Click sound player setup
        self.click_sound_uri = 'winxp-click/start.wav'  # Path to your click sound file
        self.init_click_sound_player()

        self.connect("destroy", self.on_destroy)

        # Track the number of times the next button is pressed
        self.next_button_click_count = 0

        self.show_all()

    def on_window_realized(self, widget):
        # Set the initial custom cursor
        self.set_custom_cursor('winxp-imgs/arrow.png')

    def set_custom_cursor(self, cursor_path):
        if os.path.isfile(cursor_path):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(cursor_path)
            cursor = Gdk.Cursor.new_from_pixbuf(Gdk.Display.get_default(), pixbuf, 0, 0)
            self.get_window().set_cursor(cursor)
        else:
            print(f"Cursor file {cursor_path} not found.")

    def apply_gtk_theme(self, theme_path):
        if os.path.isfile(theme_path):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(theme_path)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        else:
            print(f"Theme file {theme_path} not found.")

    def load_background_image(self, image_path):
        # Load and set the background image in the fixed container
        if hasattr(self, 'background_image'):
            self.fixed_container.remove(self.background_image)

        if not os.path.isfile(image_path):
            print(f"Error: {image_path} does not exist.")
            return

        background_image = Gtk.Image()
        background_pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        if background_pixbuf is None:
            print(f"Error loading image from {image_path}")
        else:
            print(f"Successfully loaded image from {image_path}")
        background_image.set_from_pixbuf(background_pixbuf)
        self.fixed_container.put(background_image, 0, 0)
        self.background_image = background_image
        self.fixed_container.show_all()

    def create_text_elements(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .title {
                font-size: 24pt;
                font-family: 'Franklin Gothic Medium';
                font-weight: bold;
                color: #FFFFFF;
                text-shadow: 4px 4px 4px #003399;
            }
            .text-primary {
                font-size: 9pt;
                font-family: Arial;
                font-weight: normal;
                color: #FFFFFF;
            }
        """)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Title text
        self.title_label = Gtk.Label(label="Welcome to Microsoft Windows")
        self.title_label.get_style_context().add_class("title")
        self.title_label.set_halign(Gtk.Align.START)
        self.title_label.set_valign(Gtk.Align.START)
        self.fixed_container.put(self.title_label, 48, 24)
        self.title_label.set_size_request(434, 77)

        # Description text
        self.desc_label = Gtk.Label(label="Thank you for purchasing Microsoft Windows XP.")
        self.desc_label.get_style_context().add_class("text-primary")
        self.desc_label.set_halign(Gtk.Align.START)
        self.desc_label.set_valign(Gtk.Align.START)
        self.fixed_container.put(self.desc_label, -69, 79)
        self.desc_label.set_size_request(500, 50)

        # Instruction text
        self.instr_label = Gtk.Label(label="Let's spend a few minutes setting up your computer.")
        self.instr_label.get_style_context().add_class("text-primary")
        self.instr_label.set_halign(Gtk.Align.START)
        self.instr_label.set_valign(Gtk.Align.START)
        self.fixed_container.put(self.instr_label, -10, 106)
        self.instr_label.set_size_request(400, 50)

        # Additional instruction text
        self.add_instr_label = Gtk.Label(label="To continue, click Next.")
        self.add_instr_label.get_style_context().add_class("text-primary")
        self.add_instr_label.set_halign(Gtk.Align.START)
        self.add_instr_label.set_valign(Gtk.Align.START)
        self.fixed_container.put(self.add_instr_label, -76, 370)
        self.add_instr_label.set_size_request(300, 50)

    def init_video_player(self):
        self.video_overlay = Gtk.DrawingArea()
        self.fixed_container.put(self.video_overlay, 0, 0)  # Set position to cover the whole window
        self.video_overlay.set_size_request(782, 495)  # Set size to cover the whole window

        # Create a Gst pipeline
        self.pipeline = Gst.Pipeline.new("video_pipeline")

        # Create elements
        self.source = Gst.ElementFactory.make("uridecodebin", "video_source")
        self.videoscale = Gst.ElementFactory.make("videoscale", "video_scaler")
        self.videoconvert = Gst.ElementFactory.make("videoconvert", "video_converter")
        self.capsfilter = Gst.ElementFactory.make("capsfilter", "caps_filter")
        self.sink = Gst.ElementFactory.make("glimagesink", "video_sink")

        # Configure elements
        self.source.set_property("uri", f"file://{os.path.abspath(self.video_uri)}")

        # Set caps for scaling
        caps = Gst.Caps.from_string("video/x-raw, width=782, height=495")
        self.capsfilter.set_property("caps", caps)

        # Add elements to pipeline
        self.pipeline.add(self.source)
        self.pipeline.add(self.videoscale)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.capsfilter)
        self.pipeline.add(self.sink)

        # Link elements
        self.source.connect("pad-added", self.on_pad_added)
        self.videoscale.link(self.videoconvert)
        self.videoconvert.link(self.capsfilter)
        self.capsfilter.link(self.sink)

        # Set up message handling
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.video_overlay.connect("realize", self.on_video_overlay_realize)

        # Start playing
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_pad_added(self, src, pad):
        sink_pad = self.videoscale.get_static_pad("sink")
        pad.link(sink_pad)

    def on_video_overlay_realize(self, widget):
        window = widget.get_window()
        window.ensure_native()
        xid = window.get_xid()
        if xid:
            GstVideo.VideoOverlay.set_window_handle(self.sink, xid)
        else:
            print("Could not get XID for the video overlay window")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)  # Stop video playback
            self.clear_video_overlay()  # Clear video overlay
            self.switch_to_ui()  # Switch back to UI after video ends
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}. Debugging info: {debug}")
            self.pipeline.set_state(Gst.State.NULL)

    def clear_video_overlay(self):
        # Clear the drawing area by hiding it
        self.video_overlay.hide()

    def switch_to_ui(self):
        # Implement switching back to UI logic here
        print("Switching back to UI after video ends")

    def init_music_player(self, music_uri):
        self.music_player = Gst.ElementFactory.make("playbin", "music-player")
        self.music_player.set_property("uri", f"file://{os.path.abspath(music_uri)}")

        self.music_player.set_state(Gst.State.PLAYING)

    def init_click_sound_player(self):
        self.click_player = Gst.ElementFactory.make("playbin", "click-player")
        self.click_player.set_property("uri", f"file://{os.path.abspath(self.click_sound_uri)}")

    def play_click_sound(self):
        self.click_player.set_state(Gst.State.NULL)  # Stop any previous instances
        self.click_player.set_state(Gst.State.PLAYING)

    def on_next_button_clicked(self, widget, event):
        print("Next button clicked!")
        self.play_click_sound()  # Play click sound
        self.set_wait_cursor()
        self.next_button_click_count += 1

        if self.next_button_click_count == 1:
            self.update_text_elements("Setup Your Preferences", "Choose your preferred settings.",
                                      "You can customize your settings here.", "To apply the settings, click Next.")
            self.update_next_button_image()
            self.reset_cursor_later()
        elif self.next_button_click_count == 2:
            self.update_text_elements("Confirm Your Settings", "Please review your settings.",
                                      "Make sure everything is correct.", "To proceed, click Next.")
            self.update_next_button_image()
            self.reset_cursor_later()
        elif self.next_button_click_count == 3:
            self.update_text_elements("Installing Theme", "Please wait while the theme is being installed.",
                                      "", "")
            self.next_label.set_markup('<span foreground="white" font="Tahoma 10"><u>F</u>inish</span>')
            self.set_disabled_button_image()
            self.run_install_script()
        elif self.next_button_click_count == 4:
            self.update_text_elements("Installation Complete", "The theme has been installed successfully.",
                                      "", "Click Finish to exit.")
            self.next_label.set_markup('<span foreground="white" font="Tahoma 10"><u>F</u>inish</span>')
            self.update_next_button_image()
            threading.Timer(1, Gtk.main_quit).start()

    def update_next_button_image(self):
        new_pixbuf = GdkPixbuf.Pixbuf.new_from_file('winxp-imgs/continue_clicked.png')
        new_pixbuf = new_pixbuf.scale_simple(30, 30, GdkPixbuf.InterpType.BILINEAR)
        self.next_button_image.set_from_pixbuf(new_pixbuf)
        self.next_button_image.queue_draw()

        # Schedule the button image to change back to 'continue.png' after a few seconds
        threading.Timer(1, self.reset_button_image).start()

    def reset_button_image(self):
        new_pixbuf = GdkPixbuf.Pixbuf.new_from_file('winxp-imgs/continue.png')
        new_pixbuf = new_pixbuf.scale_simple(30, 30, GdkPixbuf.InterpType.BILINEAR)
        self.next_button_image.set_from_pixbuf(new_pixbuf)
        self.next_button_image.queue_draw()

    def update_text_elements(self, title, desc, instr, add_instr):
        self.title_label.set_text(title)
        self.desc_label.set_text(desc)
        self.instr_label.set_text(instr)
        self.add_instr_label.set_text(add_instr)

    def run_install_script(self):
        print("Running installation script!")
        self.set_wait_cursor()
        install_process = subprocess.Popen("./install.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        threading.Thread(target=self.monitor_installation, args=(install_process,)).start()

    def monitor_installation(self, process):
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        process.stdout.close()
        process.wait()
        if process.returncode == 0:
            self.on_installation_complete()
        else:
            for line in iter(process.stderr.readline, ''):
                print(line, end='')
            process.stderr.close()
            print(f"Installation failed with error code: {process.returncode}")

    def on_installation_complete(self):
        print("Installation completed successfully!")
        self.update_text_elements("Installation Complete", "The theme has been installed successfully.",
                                  "", "Click Finish to exit.")
        self.event_box.set_sensitive(True)
        self.next_button_click_count = 3  # Ensure the next click exits the application
        self.reset_button_image()  # Ensure the button image is 'continue.png'
        self.reset_cursor()

    def set_disabled_button_image(self):
        new_pixbuf = GdkPixbuf.Pixbuf.new_from_file('winxp-imgs/continue_disabled.png')
        new_pixbuf = new_pixbuf.scale_simple(30, 30, GdkPixbuf.InterpType.BILINEAR)
        self.next_button_image.set_from_pixbuf(new_pixbuf)
        self.next_button_image.queue_draw()
        self.event_box.set_sensitive(False)

    def set_wait_cursor(self):
        self.set_custom_cursor('winxp-imgs/busy.png')

    def reset_cursor(self):
        self.set_custom_cursor('winxp-imgs/arrow.png')

    def reset_cursor_later(self):
        threading.Timer(1.0, self.reset_cursor).start()

    def on_destroy(self, widget):
        self.pipeline.set_state(Gst.State.NULL)
        self.music_player.set_state(Gst.State.NULL)
        Gtk.main_quit()

if __name__ == "__main__":
    Gst.init(None)
    win = XPWelcomeWindow()
    Gtk.main()
