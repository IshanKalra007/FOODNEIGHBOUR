from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

import Backend.Functions.UsersFunc as UsersFunc
from Backend.Class.CurrentUser import CurrentUser
from Frontend.CustomTools.CustomWidgets import CustomScreen, ValidationField, user_data_field_helper, password_field_helper, \
    confirm_password_field_helper
from Frontend.CustomTools.UserWidgets import open_profile_picture_popup


class EditDetailsScreen(CustomScreen):

    # Inherited Methods
    def __init__(self, **kwargs):
        super(EditDetailsScreen, self).__init__(**kwargs)
        self.app.custom_screens['EditDetails'] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = False

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()
        self.app.reload_current_user()

    def on_leave(self):
        super().on_leave()

    def clear_screen(self):
        super().clear_screen()

    def build_screen(self):
        super().build_screen()

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        box_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=20, spacing=10)
        box_layout.bind(minimum_height=box_layout.setter('height'))

        # UPDATE PROFILE PICTURE
        picture_label = MDLabel(text="Change Profile Picture", font_style="H6", size_hint_y=None,
                                height=30, halign='center')

        picture_button = MDRaisedButton(text="Select Picture", size_hint_y=None,
                                        height=50, pos_hint={'center_x': 0.5})
        picture_button.bind(on_release=open_profile_picture_popup)

        # UPDATE EMAIL
        email_label = MDLabel(text="Change Email", font_style="H6", size_hint_y=None,
                              height=30, halign='center')

        self.validation_fields["EmailField"] = ValidationField(
            text_field_widget=Builder.load_string(user_data_field_helper),
            label="Email", validation_check="UsersFunc.verify_email_reg", time_to_stop_typing=0.5)

        email_button = MDRaisedButton(text="Update Email", size_hint_y=None,
                                      height=50, pos_hint={'center_x': 0.5})
        email_button.bind(on_release=self.set_email)

        # UPDATE PASSWORD
        password_label = MDLabel(text="Change Password", font_style="H6", size_hint_y=None,
                                 height=30, halign='center')

        self.validation_fields["CurrentPasswordField"] = ValidationField(
            text_field_widget=Builder.load_string(password_field_helper).children[1],
            label="Current Password",
            validation_check="UsersFunc.verify_password")
        self.validation_fields["NewPasswordField"] = ValidationField(
            text_field_widget=Builder.load_string(password_field_helper).children[1],
            label="New Password",
            validation_check="UsersFunc.verify_password")
        self.validation_fields["ConfirmPasswordField"] = ValidationField(
            text_field_widget=Builder.load_string(confirm_password_field_helper),
            label="Confirm Password",
            validation_check="self.screen.validate_confirm_password", screen=self,
            wait_for_input_to_validate=False, required=True)

        password_button = MDRaisedButton(text="Update Password", size_hint_y=None,
                                         height=50, pos_hint={'center_x': 0.5})
        password_button.bind(on_release=self.set_password)

        # UPDATE POSTCODE
        postcode_label = MDLabel(text="Change Postcode", font_style="H6", size_hint_y=None,
                                 height=30, halign='center')

        self.validation_fields['PostcodeField'] = ValidationField(
            text_field_widget=Builder.load_string(user_data_field_helper),
            label="Postcode", validation_check="UsersFunc.verify_postcode")

        postcode_button = MDRaisedButton(text="Update Postcode", size_hint_y=None,
                                         height=50, pos_hint={'center_x': 0.5})
        postcode_button.bind(on_release=self.set_postcode)

        # UPDATE PHONE NUMBER
        phone_label = MDLabel(text="Change Phone Number", font_style="H6", size_hint_y=None,
                              height=30, halign='center')

        self.validation_fields['PhoneField'] = ValidationField(
            text_field_widget=Builder.load_string(user_data_field_helper),
            label="Phone Number", validation_check="UsersFunc.verify_phone")

        phone_button = MDRaisedButton(text="Update Phone Number", size_hint_y=None,
                                      height=50, pos_hint={'center_x': 0.5})
        phone_button.bind(on_release=self.set_phone)


        # Add all widgets
        box_layout.add_widget(picture_label)
        box_layout.add_widget(picture_button)
        box_layout.add_widget(email_label)
        box_layout.add_widget(self.validation_fields["EmailField"].text_field)
        box_layout.add_widget(email_button)
        box_layout.add_widget(password_label)
        box_layout.add_widget(self.validation_fields['CurrentPasswordField'].text_field.parent)
        box_layout.add_widget(self.validation_fields['NewPasswordField'].text_field.parent)
        box_layout.add_widget(self.validation_fields['ConfirmPasswordField'].text_field)
        box_layout.add_widget(password_button)
        box_layout.add_widget(postcode_label)
        box_layout.add_widget(self.validation_fields['PostcodeField'].text_field)
        box_layout.add_widget(postcode_button)
        box_layout.add_widget(phone_label)
        box_layout.add_widget(self.validation_fields['PhoneField'].text_field)
        box_layout.add_widget(phone_button)

        scroll_view.add_widget(box_layout)
        self.main_space.add_widget(scroll_view)

    # Validate whether the new password and confirmed passwords are identical.
    def validate_confirm_password(self, obj):
        new_password = self.validation_fields['NewPasswordField'].text
        confirm_password = self.validation_fields['ConfirmPasswordField'].text
        if new_password == confirm_password:
            return True
        else:
            return 'Passwords must match'

    # Set password using backend function
    def set_password(self, obj):
        password = self.validation_fields['ConfirmPasswordField'].text
        current_password = self.validation_fields['CurrentPasswordField'].text
        if (UsersFunc.verify_password(password) != 'Invalid Password'
                and UsersFunc.verify_current_password(current_password, CurrentUser().current_user.user_id) != 'Current password does not match'
                and self.validate_confirm_password(password)):
            obj.disabled = True
            obj.text = 'Password Updated'
            UsersFunc.update_password(password, CurrentUser().current_user.user_id)

    # Set email using backend function
    def set_email(self, obj):
        email = self.validation_fields['EmailField'].text
        if UsersFunc.verify_email_reg(email) not in ('Email already registered', 'Invalid email'):
            obj.disabled = True
            obj.text = 'Email Updated'
            UsersFunc.update_email(email, CurrentUser().current_user.user_id)

    # Set postcode using backend function
    def set_postcode(self, obj):
        postcode = self.validation_fields['PostcodeField'].text
        if UsersFunc.verify_postcode(postcode) != 'Invalid Postcode':
            obj.disabled = True
            obj.text = 'Postcode Updated'
            UsersFunc.update_postcode(postcode, CurrentUser().current_user.user_id)

    # Set phone number using backend function
    def set_phone(self, obj):
        phone = self.validation_fields['PhoneField'].text
        if UsersFunc.verify_phone(phone) != 'Invalid Phone Number':
            obj.disabled = True
            obj.text = 'Phone Number Updated'
            UsersFunc.update_phone(phone, CurrentUser().current_user.user_id)
