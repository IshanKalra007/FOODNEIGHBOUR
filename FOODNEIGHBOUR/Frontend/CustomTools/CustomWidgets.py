from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar

from functools import partial
from geopy.geocoders import Nominatim

from Backend.Class.CurrentUser import CurrentUser
import Backend.Functions.UsersFunc as UsersFunc  # Needed for running evals on validation field validation checks

back_button_helper = """
MDIconButton:
        pos_hint: {'center_x' : 0.1, 'center_y': 0.95}
        on_release: app.go_back()
        icon: 'keyboard-return'
"""
page_scroll_view_helper = """
#:import ScrollEffect  kivy.effects.scroll.ScrollEffect
ScrollView:
    effect_y: ScrollEffect() #To prevent default bouncy dampening effect
    always_overscroll: True
    do_scroll_x: False
    overscroll:0
    size_hint: (0.95,1)
    pos_hint: {'center_x' : 0.5}
    pos_hint_y: None
    pos: (0, -40)
    FloatLayout:
        id: sec_layout
        padding: 8
        size_hint_y: None  # this is required for scrolling
        height: 200
"""


class CustomScreen(Screen):
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super(CustomScreen, self).__init__(**kwargs)
        self.main_space = None
        self.scroll_space = None
        self.top_seq_y = 0.95
        self.cur_sequential_widget_y = self.top_seq_y
        self.is_built = False

        self.scrollable = False
        self.rebuild_on_load = False
        self.has_back_button = False

        self.validation_fields = {}

    def on_pre_enter(self, *args):
        super().on_pre_enter()

        self.active = True
        if (self.rebuild_on_load or not (
                self.is_built)):  # Build only if not built or this screen has rebuilding enabled
            self.build_screen()

        return 0

    def on_leave(self, *args):
        if self.rebuild_on_load and self.is_built:  # Clear only if built or rebuilding enabled
            self.clear_screen()
        self.active = False

        super().on_leave()

    def refresh_screen(self):
        self.clear_screen()
        self.build_screen()

    def build_screen(self):
        has_main_space = False
        for id in self.ids:
            if id == 'main_space':
                has_main_space = True
        if not has_main_space:
            return False

        if self.is_built:
            self.clear_screen()  # Reset if already built
        self.main_space = self.ids.main_space
        self.cur_sequential_widget_y = self.top_seq_y  # Reset the top position for new sequential widgets
        self.is_built = True

        if self.scrollable:
            self.scroll_space = Builder.load_string(page_scroll_view_helper).children[0]
            self.main_space.add_widget(self.scroll_space.parent)

        if self.has_back_button:
            self.main_space.add_widget(Builder.load_string(back_button_helper))
        return True

    def clear_screen(self):
        self.main_space = self.ids.main_space
        while len(self.main_space.children) > 0:
            self.main_space.remove_widget(self.main_space.children[0])
        self.is_built = False

    def sequential_add_widget(self, widget, spacing=0.12):
        self.main_space.add_widget(widget)
        self.cur_sequential_widget_y -= spacing
        widget.pos_hint = {'center_x': 0.5, 'center_y': self.cur_sequential_widget_y}
        return widget

    def box_add_widget(self, widget):
        self.main_space.add_widget(widget)
        return widget

    def on_point_three_update(self, run_time):
        self.update_validation_fields(run_time)

    def update_validation_fields(self, run_time):
        vfs_to_remove = []
        # Continually check input fields for changing text since there is no inbuilt on_text_change event
        for vf in self.validation_fields:
            if self.validation_fields[vf].text_field is not None and self.is_built:
                self.validation_fields[vf].check_for_change(run_time)
            else:  # Stop updating validation fields that are no longer in operation
                vfs_to_remove.append(vf)
        for vf in vfs_to_remove:  # Cleanup redundant fields
            val_field = self.validation_fields[vf]
            if (val_field.text_field != None): del val_field.text_field
            del self.validation_fields[vf]
            del val_field

    def validate_all_fields(self):
        passed_all_checks = True
        for vf in self.validation_fields:
            passed_all_checks = passed_all_checks and str(self.validation_fields[vf].validate_field()) == "True"
        return passed_all_checks


label_helper_1 = """
MDLabel:
    text:"Label"
    size_hint:(1, None)
    font_size: 14
    halign:'center'
    height:dp(26)  # Adjust the height as needed
"""


def generate_label(text, font_size=15, helper_index=1, height=20, valign="bottom", font_style="Body1"):
    label = Builder.load_string(label_helper_1)
    label.font_size = font_size
    label.font_style = font_style
    label.text = text
    label.height = height
    label.valign = valign
    return label


user_data_field_helper = """
MDTextField:
    hint_text: "Email"
    helper_text: ""
    #icon_right: "android"
    #icon_right_color: app.theme_cls.primary_color
    helper_text_mode: "on_focus"
    pos_hint:{'center_x': 0.5, 'center_y': 0.8}
    size_hint_x:None
    width:200
"""

search_field_helper = """
MDTextField:
    hint_text: "Search"
    helper_text: ""
    #icon_right: "android"
    #icon_right_color: app.theme_cls.primary_color
    helper_text_mode: "on_focus"
    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
    size_hint_x:None
    width:200
    anchor_x: 'center'
    anchor_y: 'top'
    
"""

password_field_helper = """
MDRelativeLayout:
    size_hint_y:None
    height: 50
    MDTextField:
        id: password_field
        hint_text: "Password"
        helper_text: "...."
        helper_text_mode: "on_focus"
        size_hint_x:None
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        #icon_right : "eye-off"
        width:200
        password: True
    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: password_field.width - self.width + dp(60), 0
        theme_text_color: "Hint"
        on_release:
            password_field.password = True if password_field.password is False else False
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
"""

confirm_password_field_helper = """
MDTextField:
        hint_text: "Confirm Password"
        helper_text: "Passwords must be identical"
        helper_text_mode: "on_focus"
        size_hint_x:None
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        #icon_right : "eye-off"
        width:200
        password: True
"""


class ValidationField:
    def __init__(self, text_field_widget, label, validation_check='', default_text="", max_text_length=50,
                 min_text_length=0, required=True, time_to_stop_typing=0.2, screen=None,
                 wait_for_input_to_validate=True, helper_text=''):

        self.text_field = text_field_widget
        self.text_field.text = default_text
        self.text_field.helper_text = helper_text
        self.text_field.hint_text = label
        self.max_text_length = max_text_length
        self.min_text_length = min_text_length

        self.validation_check = validation_check
        self.required = required
        self.time_to_stop_typing = time_to_stop_typing

        self.text = default_text
        self.helper_text = helper_text
        self.last_time_changed = 0
        self.has_validated_new_text = True
        self.text_field.helper_text_mode = "on_error"
        self.screen = screen
        self.wait_for_input_to_validate = wait_for_input_to_validate

    def check_for_change(self, run_time):
        detected_stop_type = False
        if self.wait_for_input_to_validate or self.text == "":
            if self.text_field.text != self.text:
                self.text = self.text_field.text
                self.has_validated_new_text = False  # Trigger to validate once user stopped typing
                self.last_time_changed = run_time

            # Only validate once user has stopped typing to prevent database spamming
            # (e.g. checking email is not in database)
            if not self.has_validated_new_text and run_time - self.last_time_changed > self.time_to_stop_typing:
                self.text = self.text_field.text
                self.validate_field()
                detected_stop_type = True
        else:
            self.text = self.text_field.text
            self.validate_field()
        return detected_stop_type

    def error(self, message):
        self.text_field.error = True
        self.text_field.helper_text = message

        return "[" + self.text_field.hint_text + "Field]:" + message

    def clear_error(self):
        self.text_field.error = False
        self.text_field.text_color_normal = (0.3, 0.3, 0.3, 1)  # Set non focused, validated text color as black
        self.text_field.helper_text = self.helper_text

        return True

    def validate_field(self):
        self.has_validated_new_text = True
        if self.text != "":
            if self.max_text_length != 0 and len(self.text) > self.max_text_length:
                return self.error("Surpassed character limit of " + str(self.max_text_length))
            validation = "True"
            if self.validation_check != "":
                validation = str(eval(self.validation_check)(self.text))
            if validation == "True":
                return self.clear_error()
            else:
                return self.error(validation)
        elif self.required:
            return self.error("Required field cannot be left blank")
        else:
            return self.clear_error()


dropdown_button_helper = """
Button
    text: 'dropdown'
    size_hint: None, None
    size: 200, 40      
"""
dropdown_helper = """
DropDown:
    on_kv_post: self.dismiss()
"""
dropdown_option_helper = """
Button:
    text: 'Descending'
    size_hint_y: None
    height: 30
"""


# Makes a dropdown widget to given specifications
def generate_dropdown(label_text, options, parent=None, auto_label=True, opt_index=0, button=None, set_on_release=True,
                      return_button=True):
    if button is None:
        button = Builder.load_string(dropdown_button_helper)
        button.text = options[opt_index]
    if auto_label and parent != None:
        label = Builder.load_string(label_helper_1)
        label.text = label_text
        parent.add_widget(label)

    dropdown = Builder.load_string(dropdown_helper)

    for o in options:
        option = Builder.load_string(dropdown_option_helper)
        option.text = o
        if set_on_release:
            option.on_press = partial(set_widget_text, button,
                                      o)
            option.on_release = dropdown.dismiss
        option.background_normal = 'White'
        option.background_color = (0.7, 0.7, 0.7, 1)
        option.color = (0, 0, 0, 1)
        dropdown.add_widget(option)

    if set_on_release:
        button.on_release = partial(dropdown.open, button)
    if parent is not None:
        parent.add_widget(button)
    if return_button:
        return button
    else:
        return dropdown


# Gets list of locations relating to given query
def get_possible_locations(query, limit=5):
    try:
        loc = Nominatim(user_agent="GetLoc")
        return loc.geocode(query, exactly_one=False, limit=limit, addressdetails=False, language=False,
                           geometry=None, extratags=False, country_codes=None, viewbox=None, bounded=False,
                           featuretype=None,
                           namedetails=False)
    except:
        print("Failed to connect to geopy")
        return None


def get_location_from_coords(coords):
    try:
        geolocator = Nominatim(user_agent="GetLoc")
        return geolocator.reverse(coords, exactly_one=True)
    except:
        print("Failed to connect to geopy")
        return None


# Provides functionality to search and suggest possible locations as well as store their coordinates
class LocationPicker:
    def __init__(self, default_coords=None):
        self.cur_coords = default_coords

        self.location_field = ValidationField(text_field_widget=Builder.load_string(user_data_field_helper),
                                              label="Your Location",
                                              min_text_length=1,
                                              max_text_length=1000, helper_text='')
        self.has_valid_coords = False
        if default_coords is not None: self.set_location()

        self.options_dropdown = None

    def on_point_three_update(self, run_time):
        stopped_typing = self.location_field.check_for_change(run_time)
        if stopped_typing:
            self.cur_coords = None
            self.location_string = self.location_field.text_field.text
            if self.location_string != "": self.generate_options_dropdown()

    def set_location(self, coords=None):
        if coords is not None:
            self.cur_coords = coords
        if self.cur_coords is not None:
            location = get_location_from_coords(self.cur_coords)
            if location is not None:
                self.location_field.text_field.text = location.address
                self.location_field.text = location.address
                self.location_field.clear_error()

    def verify_location_text(self):
        self.location_string = self.location_field.text_field.text
        p_locations = get_possible_locations(self.location_string)
        if p_locations is not None and len(p_locations) > 0:
            self.cur_coords = (p_locations[0].latitude, p_locations[0].longitude)
            self.location_field.clear_error()
            self.has_valid_coords = True
        else:
            self.location_field.error("Invalid Location")
            self.has_valid_coords = False

    def generate_options_dropdown(self):
        p_locations = get_possible_locations(self.location_string)
        if p_locations is not None and len(p_locations) > 0:
            option_strings = []
            for p_location in p_locations:
                option_string = p_location.address
                option_string = (option_string[:25] + '..') if len(option_string) > 25 else option_string
                option_strings.append(option_string)
            print(option_strings)
            if self.options_dropdown is not None and self.options_dropdown.parent is not None:
                self.options_dropdown.dismiss()
                self.options_dropdown.parent.remove_widget(self.options_dropdown);
                del self.options_dropdown
            self.options_dropdown = generate_dropdown("", option_strings, parent=None, auto_label=False,
                                                      button=self.location_field.text_field, set_on_release=False,
                                                      return_button=False)
            i = len(p_locations) - 1
            for option in self.options_dropdown.children[0].children:
                option.on_release = partial(self.select_location, p_locations[i].address,
                                            (p_locations[i].latitude, p_locations[i].longitude))
                i -= 1

            Clock.schedule_once(self.open_options_dropdown, 0.05)

    def open_options_dropdown(self, d=None):
        self.options_dropdown.open(self.location_field.text_field)

    def select_location(self, text, coords, d=None):
        self.options_dropdown.dismiss()
        print("selected " + text)
        self.location_field.text_field.text = text
        self.location_field.text = text  # Setting both prevents change detection and opening dropdown again
        self.cur_coords = coords
        if CurrentUser().current_user is not None:
            CurrentUser().current_user.location = coords


# can be used by buttons e.g: on_release=partial(set_widget_text,widget,text)
def set_widget_text(widget, text):
    widget.text = text


# snackbar pop-up to display message for short period of time
def show_snackbar(message, duration=1):
    label = MDLabel(text=message, font_size='16sp')
    snackbar = Snackbar(duration=duration)
    snackbar.add_widget(label)
    snackbar.open()


link_button_helper = """
MDFlatButton:
        text: "Link"
        pos_hint: {'center_x' : 0.5, 'center_y': 0.1}
        theme_text_color: "Custom"
        text_color: app.link_color
"""
