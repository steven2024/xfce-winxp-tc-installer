import gi
import os
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class ResizableLabel(Gtk.EventBox):
    def __init__(self, text, style_class, x, y, width, height, update_callback):
        super().__init__()
        self.set_above_child(True)
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_MOTION_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK)

        self.label = Gtk.Label(label=text)
        self.label.get_style_context().add_class(style_class)
        self.add(self.label)

        self.resize_mode = None
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.set_size_request(width, height)
        self.connect("button-press-event", self.on_button_press)
        self.connect("motion-notify-event", self.on_motion_notify)
        self.connect("button-release-event", self.on_button_release)

        self.fixed_container = None
        self.update_callback = update_callback

    def set_fixed_container(self, container):
        self.fixed_container = container

    def on_button_press(self, widget, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        allocation = self.get_allocation()
        if event.button == 1:  # Left-click to move
            self.resize_mode = "move"
        elif event.button == 3:  # Right-click to resize
            self.resize_mode = "resize"

    def on_motion_notify(self, widget, event):
        if self.resize_mode == "move":
            new_x = self.fixed_container.child_get_property(self, 'x') + (event.x - self.drag_start_x)
            new_y = self.fixed_container.child_get_property(self, 'y') + (event.y - self.drag_start_y)
            self.fixed_container.move(self, new_x, new_y)
            self.update_callback()
        elif self.resize_mode == "resize":
            new_width = max(self.get_allocated_width() + (event.x - self.drag_start_x), 10)
            new_height = max(self.get_allocated_height() + (event.y - self.drag_start_y), 10)
            self.set_size_request(new_width, new_height)
            self.update_callback()

    def on_button_release(self, widget, event):
        self.resize_mode = None
        self.update_callback()

    def update_position_and_size(self, x, y, width, height):
        self.fixed_container.move(self, x, y)
        self.set_size_request(width, height)
        self.update_callback()

class ObserverWindow(Gtk.Window):
    def __init__(self, labels, update_callback):
        Gtk.Window.__init__(self, title="Label Positions")
        self.set_default_size(400, 300)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)
        self.labels = labels
        self.update_callback = update_callback
        self.create_spin_buttons()
        self.show_all()

    def create_spin_buttons(self):
        for label_info in self.labels:
            label = label_info["widget"]
            allocation = label.get_allocation()
            label_text = label.label.get_text()
            label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

            label_name = Gtk.Label(label=label_text)
            spin_x = Gtk.SpinButton(adjustment=Gtk.Adjustment(value=label_info["x"], lower=0, upper=1000, step_increment=1), numeric=True)
            spin_y = Gtk.SpinButton(adjustment=Gtk.Adjustment(value=label_info["y"], lower=0, upper=1000, step_increment=1), numeric=True)
            spin_width = Gtk.SpinButton(adjustment=Gtk.Adjustment(value=allocation.width, lower=10, upper=1000, step_increment=1), numeric=True)
            spin_height = Gtk.SpinButton(adjustment=Gtk.Adjustment(value=allocation.height, lower=10, upper=1000, step_increment=1), numeric=True)

            spin_x.connect("value-changed", self.on_spin_change, label_info, "x")
            spin_y.connect("value-changed", self.on_spin_change, label_info, "y")
            spin_width.connect("value-changed", self.on_spin_change, label_info, "width")
            spin_height.connect("value-changed", self.on_spin_change, label_info, "height")

            label_box.pack_start(label_name, False, False, 0)
            label_box.pack_start(Gtk.Label(label="X:"), False, False, 0)
            label_box.pack_start(spin_x, False, False, 0)
            label_box.pack_start(Gtk.Label(label="Y:"), False, False, 0)
            label_box.pack_start(spin_y, False, False, 0)
            label_box.pack_start(Gtk.Label(label="Width:"), False, False, 0)
            label_box.pack_start(spin_width, False, False, 0)
            label_box.pack_start(Gtk.Label(label="Height:"), False, False, 0)
            label_box.pack_start(spin_height, False, False, 0)

            self.box.pack_start(label_box, False, False, 0)

    def on_spin_change(self, spin_button, label_info, attribute):
        label = label_info["widget"]
        allocation = label.get_allocation()

        if attribute == "x":
            label_info["x"] = spin_button.get_value_as_int()
        elif attribute == "y":
            label_info["y"] = spin_button.get_value_as_int()
        elif attribute == "width":
            allocation.width = spin_button.get_value_as_int()
        elif attribute == "height":
            allocation.height = spin_button.get_value_as_int()

        label.update_position_and_size(label_info["x"], label_info["y"], allocation.width, allocation.height)
        self.update_callback()

class XPWelcomeWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="XP OOBE Theme Installer")
        self.set_default_size(782, 495)
        
        self.fixed_container = Gtk.Fixed()
        self.add(self.fixed_container)

        # Load the background image
        self.current_background = 'winxp-imgs/Bitmap20142.jpg'
        self.load_background_image(self.current_background)

        # Create and place text elements
        self.create_text_elements()

        # Create next button
        self.create_next_button()

        # Create print positions button
        self.create_print_button()

        # Observer window
        self.observer_window = ObserverWindow(self.labels, self.update_observer_window)
        self.observer_window.show_all()
        self.update_observer_window()

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def load_background_image(self, image_path):
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
                text-shadow: 4px 4px 2px #003399; /* Offset, slight blur radius, and color */
                padding: 20px 0; /* Adjust this to control the height */
            }

            .description {
                font-size: 9pt;
                font-family: Tahoma;
                color: white;
            }

            .instruction {
                font-size: 9pt;
                font-family: Arial;
                color: white;
            }
        """)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.labels = [
            {"widget": self.create_label("Welcome to Microsoft Windows", "title", 20, 20, 300, 50), "x": 20, "y": 20},
            {"widget": self.create_label("Thank you for purchasing this computer featuring Microsoft Windows XP.", "description", 20, 60, 500, 50), "x": 20, "y": 60},
            {"widget": self.create_label("Let's spend a few minutes setting up your computer.", "instruction", 20, 90, 400, 50), "x": 20, "y": 90},
            {"widget": self.create_label("To continue, click Next.", "instruction", 20, 130, 300, 50), "x": 20, "y": 130},
        ]

    def create_label(self, text, style_class, x, y, width, height):
        label = ResizableLabel(text, style_class, x, y, width, height, self.update_observer_window)
        label.set_fixed_container(self.fixed_container)
        self.fixed_container.put(label, x, y)
        return label

    def create_next_button(self):
        event_box = Gtk.EventBox()
        event_box.set_size_request(30, 30)

        next_button_image = Gtk.Image()
        next_button_pixbuf = GdkPixbuf.Pixbuf.new_from_file('winxp-imgs/continue.png')
        next_button_pixbuf = next_button_pixbuf.scale_simple(30, 30, GdkPixbuf.InterpType.BILINEAR)
        next_button_image.set_from_pixbuf(next_button_pixbuf)
        event_box.add(next_button_image)

        next_label = Gtk.Label()
        next_label.set_markup('<span foreground="white" font="Tahoma 10"><u>N</u>ext</span>')
        next_label.set_halign(Gtk.Align.START)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.pack_start(next_label, False, False, 0)
        hbox.pack_start(event_box, False, False, 0)

        button_x = 782 - 30 - 10
        button_y = 495 - 30 - 10

        self.fixed_container.put(hbox, button_x - 60, button_y)

        event_box.connect("button-press-event", self.on_next_button_clicked)

    def create_print_button(self):
        print_button = Gtk.Button(label="Print Positions")
        print_button.connect("clicked", self.print_label_positions)
        self.fixed_container.put(print_button, 700, 450)

    def on_next_button_clicked(self, widget, event):
        print("Next button clicked!")
        installer = WinXPThemeInstaller()
        installer.run_installation()

        self.load_background_image('winxp-imgs/Bitmap20142.jpg')

        next_button_image = Gtk.Image()
        next_button_pixbuf_clicked = GdkPixbuf.Pixbuf.new_from_file('winxp-imgs/continue_clicked.png')
        next_button_pixbuf_clicked = next_button_pixbuf_clicked.scale_simple(30, 30, GdkPixbuf.InterpType.BILINEAR)
        next_button_image.set_from_pixbuf(next_button_pixbuf_clicked)
        widget.get_children()[0].destroy()
        widget.add(next_button_image)

        self.fixed_container.move(widget, 782 - 30 - 10 - 60, 495 - 30 - 10)

    def play_audio(self, audio_file):
        pipeline_str = f"filesrc location={audio_file} ! decodebin ! audioconvert ! autoaudiosink"
        self.player = Gst.parse_launch(pipeline_str)
        self.player.set_state(Gst.State.PLAYING)

    def print_label_positions(self, button):
        for label in self.labels:
            allocation = label["widget"].get_allocation()
            print(f"Label: {label['widget'].label.get_text()}")
            print(f"Position: ({allocation.x}, {allocation.y})")
            print(f"Size: ({allocation.width}, {allocation.height})")
            print("")

    def update_observer_window(self):
        self.observer_window.create_spin_buttons()

class WinXPThemeInstaller:
    def __init__(self):
        self.installation_status = ""

    def run_installation(self):
        try:
            # Execute the main installation script
            subprocess.run(['sudo', './install.sh'])
            self.update_status("Installation completed successfully!")
        except Exception as e:
            self.update_status(f"Error installing WinXP Theme: {str(e)}")

    def update_status(self, message):
        self.installation_status = message

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    win = XPWelcomeWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
