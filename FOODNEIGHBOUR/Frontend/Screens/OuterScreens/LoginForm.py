from kivy.lang import Builder
import Backend.Functions.UsersFunc as UsersFunc
from Backend.Class.CurrentUser import CurrentUser
from Frontend.CustomTools.CustomWidgets import (CustomScreen, password_field_helper, user_data_field_helper,
                                                ValidationField, LocationPicker)

buttons_helper = """
FloatLayout:
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x' : 0.5, 'center_y': 0.4}
        on_release:
            app.custom_screens["Login"].submit_login_details()
    MDFlatButton:
        text: "Don't have an account? Sign up..."
        pos_hint: {'center_x' : 0.5, 'center_y': 0.1}
        on_release: app.change_outer_screen('register_details')
        theme_text_color: "Custom"
        text_color: app.link_color
    
    # MDRectangleFlatButton:
    #     text: 'DebugFill'
    #     pos_hint: {'center_x' : 0.5, 'center_y': 0.2}
    #     on_release:
    #         app.custom_screens["Login"].debug_fill_details()
"""

error_message_helper="""
MDLabel:
    text: ''
    halign: "center"    
    color: (0.8,0.2,0.2,1)
    font_size: 13
"""


class LoginScreen(CustomScreen):

    # Inherited Methods
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app.custom_screens["Login"] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = True

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def build_screen(self):
        if not (super().build_screen()):
            return False
        super().build_screen()

        # Input Fields
        self.validation_fields["EmailField"] = ValidationField(
            text_field_widget=self.sequential_add_widget(Builder.load_string(user_data_field_helper)),
            label="Email", validation_check="UsersFunc.validate_email_login")
        self.validation_fields["PasswordField"] = ValidationField(
            text_field_widget=self.sequential_add_widget(Builder.load_string(password_field_helper)).children[1],
            # Get textfield of password component
            label="Password", validation_check="")

        # Debug Location setting to be replaced once automatic GPS tracking is introduced
        self.debug_location_picker = LocationPicker()
        self.debug_location_picker.location_field.text_field.pos_hint= {'center_x' : 0.5, 'center_y': 0.3}
        self.sequential_add_widget(self.debug_location_picker.location_field.text_field)
        self.debug_location_picker.location_field.text_field.hint_text="GPS Location"

        # Message label to be used upon failure to log in
        self.access_denied_message = self.sequential_add_widget(Builder.load_string(error_message_helper), spacing=0.08)
        self.access_denied_message.text = ""

        # Buttons (Sign In, Debug Login, Sign up)
        self.main_space.add_widget(Builder.load_string(buttons_helper))

        return True

    def clear_screen(self):
        super().clear_screen()

    # Local Methods
    def submit_login_details(self):
        if self.is_built:
            self.access_denied_message.text = ""
            # Run validation checks on all fields (displays messages on each)
            valid_details = self.validate_all_fields()

            if self.debug_location_picker.cur_coords is None:
                # Don't log in and tell user bad location
                self.debug_location_picker.location_field.error("Invalid location")
            elif valid_details:
                # All details are valid so attempt login, retrieve inputs
                email = self.validation_fields["EmailField"].text
                password = self.validation_fields["PasswordField"].text

                # if the Users email and password are in db (Also sets the current user)
                if UsersFunc.authenticate_user(email, password):
                    current_user = CurrentUser().current_user
                    # When GPS getting works, replace this
                    current_user.location = self.debug_location_picker.cur_coords
                    self.app.update_nav_bar_details() # Set picture and details in nav bar
                    self.app.change_outer_screen('inner_screen')  # Go to inner view now logged in
                else:
                    self.access_denied_message.text = "Invalid email or password"

    def debug_fill_details(self):  # For debugging purposes to make logging in quicker
        self.validation_fields["EmailField"].text_field.text = "user1@gmail.com"
        self.validation_fields["PasswordField"].text_field.text = "password"
        # Set both text values for visual purposes and prevent validation detecting input change
        self.validation_fields["EmailField"].text = "user1@gmail.com"
        self.validation_fields["PasswordField"].text = "password"
        # Set location to default (Newcastle Upon Tyne)
        self.debug_location_picker.set_location((54.97384, -1.61315))

    def on_point_three_update(self, run_time):
        super().on_point_three_update(run_time)
        # Call update on location picker
        if self.is_built and self.debug_location_picker is not None:
            self.debug_location_picker.on_point_three_update(run_time)
