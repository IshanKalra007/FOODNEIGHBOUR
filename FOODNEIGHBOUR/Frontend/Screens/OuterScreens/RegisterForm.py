from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from Backend.Functions.UsersFunc import add_user
from Frontend.CustomTools.CustomWidgets import CustomScreen, password_field_helper, user_data_field_helper, \
    confirm_password_field_helper, ValidationField, show_snackbar

buttons_helper = """
MDRectangleFlatButton:
    text: 'Submit'
    on_press: app.custom_screens["Register"].submit_register_details()
    pos_hint: {'center_x': 0.5}
    spacing: 10
"""
tc_string=f'''By registering, you agree to the following terms and conditions:
1. Usage: You agree to use this app for lawful purposes only.
2. Privacy: Your personal data will be protected in accordance with our privacy policy.
3. Liability: We are not liable for any damages arising from the use of this app.
4. Changes: These terms may be updated at any time. Continued use of the app constitutes acceptance of the updated terms.
5. Contact: For any queries, contact us at support@foodshareapp.com.'''


class RegisterDetailsScreen(CustomScreen):

    # Inherited Methods
    def __init__(self, **kwargs):
        super(RegisterDetailsScreen, self).__init__(**kwargs)
        self.app.custom_screens["Register"] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 1
        self.has_back_button = False
        self.tc = False

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def build_screen(self):
        if not (super().build_screen()): return False

        # Input Fields
        self.validation_fields["UsernameField"] = ValidationField(
            text_field_widget=self.box_add_widget(Builder.load_string(user_data_field_helper)),
            label="Full Name",
            validation_check="UsersFunc.verify_username")
        self.validation_fields["EmailField"] = ValidationField(
            text_field_widget=self.box_add_widget(Builder.load_string(user_data_field_helper)),
            label="Email", validation_check="UsersFunc.verify_email_reg", time_to_stop_typing=0.5)
        self.validation_fields["PhoneNumberField"] = ValidationField(
            text_field_widget=self.box_add_widget(Builder.load_string(user_data_field_helper)),
            label="Phone Number", validation_check="UsersFunc.verify_phone")
        self.validation_fields["PostcodeField"] = ValidationField(
            text_field_widget=self.box_add_widget(Builder.load_string(user_data_field_helper)),
            label="Postcode",
            validation_check="UsersFunc.verify_postcode")
        self.validation_fields["PasswordField"] = ValidationField(
            text_field_widget=self.box_add_widget(Builder.load_string(password_field_helper)).children[1],
            label="Password",
            validation_check="UsersFunc.verify_password")
        self.validation_fields["ConfirmPasswordField"] = ValidationField(
            text_field_widget=self.box_add_widget(Builder.load_string(confirm_password_field_helper)),
            label="Confirm Password",
            validation_check="self.screen.validate_confirm_password", screen=self, wait_for_input_to_validate=False,
            required=True)

        # Terms and conditions button
        tc_dialog = MDFlatButton(text='Read the Terms and Conditions',on_release=self.tc_dialog, pos_hint={'center_x': 0.5})
        self.box_add_widget(tc_dialog)
        # Message about T&Cs
        self.tc_label = MDLabel(text='You must accept the terms and conditions.', halign='center')
        self.box_add_widget(self.tc_label)

        # Buttons (Submit)
        self.box_add_widget(Builder.load_string(buttons_helper))

        return True

    def clear_screen(self):
        super().clear_screen()

    def validate_confirm_password(self, obj):
        # Ensure passwords match
        if self.validation_fields["PasswordField"].text == self.validation_fields["ConfirmPasswordField"].text:
            return True
        else:
            return "Passwords must match"

    # Local Methods
    def submit_register_details(self):
        if self.is_built:
            valid_details = self.validate_all_fields()
            if valid_details and self.tc:
                # Retrieve all input data
                username = self.validation_fields["UsernameField"].text
                email = self.validation_fields["EmailField"].text
                phone_number = self.validation_fields["PhoneNumberField"].text
                postcode = self.validation_fields["PostcodeField"].text
                password = self.validation_fields["PasswordField"].text

                success = add_user(username, password, email, phone_number, postcode)
                if success:
                    self.app.change_outer_screen("login")
                    show_snackbar("Account Created Successfully")

    def tc_dialog(self, obj):
        self.dialog = MDDialog(title='Terms & Conditions', type='custom', content_cls=TCDialogContent(),buttons=[
                MDRaisedButton(text='Accept',on_release=self.tc_accept),
                MDRaisedButton(text='Decline',on_release=self.tc_decline)])
        tc_info = MDLabel(text=tc_string, font_size=self.width/20)
        self.dialog.content_cls.children[0].children[0].add_widget(tc_info)
        self.dialog.open()

    def tc_accept(self, obj):
        self.tc_label.opacity = 0
        self.remove_widget(self.tc_label)
        self.tc = True
        self.dialog.dismiss()

    def tc_decline(self, obj):
        self.tc_label.opacity = 1
        self.tc = False
        self.dialog.dismiss()


# Provide class to link between content_cls and class defined in root helper
class TCDialogContent(FloatLayout):
    pass
