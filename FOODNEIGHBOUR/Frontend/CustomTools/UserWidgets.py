from kivymd.app import MDApp
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton

from Backend.Class.CustomerSupport import CustomerSupport
from Frontend.CustomTools.CustomWidgets import show_snackbar

import Backend.Functions.UsersFunc as UsersFunc
from Backend.Class.CurrentUser import CurrentUser
from Main import Session


class ResponsePopup(Popup):  # custom pop-up widget for when creating a response
    def __init__(self, submit_callback, **kwargs):
        super(ResponsePopup, self).__init__(**kwargs)
        self.title = "Add a Response"
        self.size_hint = (None, None)
        self.size = (400, 300)  # Adjust the size as needed

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.response_input = TextInput(multiline=True, size_hint=(1, 0.8))
        self.layout.add_widget(self.response_input)

        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        self.submit_button = MDRaisedButton(text="Submit", size_hint=(0.3, 1))
        self.submit_button.bind(on_press=self.submit_response)
        button_layout.add_widget(self.submit_button)

        self.close_button = MDRaisedButton(text="Close", size_hint=(0.3, 1))
        self.close_button.bind(on_press=self.dismiss)
        button_layout.add_widget(self.close_button)

        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

        self.submit_callback = submit_callback

    def submit_response(self, instance):  # when response is submitted
        show_snackbar("Response Created Successfully")
        response_text = self.response_input.text
        self.submit_callback(response_text)
        self.dismiss()

class profile_picture_popup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Change Profile Picture"
        self.size_hint = (None, None)
        self.size = (dp(300), dp(350))
        self.auto_dismiss = True

        # Create the grid layout
        grid_layout = GridLayout(cols=3, padding=10, spacing=10, size_hint=(None, None))
        grid_layout.bind(minimum_height=grid_layout.setter('height'), minimum_width=grid_layout.setter('width'))

        # Add image buttons to the grid layout
        for i in range(9):
            img_btn = Button(size_hint=(None, None), size=(100, 100), background_normal=f'Images/{i+1}.png')
            img_btn.bind(on_release=self.on_image_click)
            grid_layout.add_widget(img_btn)

        # Create a box layout to center the grid layout
        box_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        box_layout.add_widget(grid_layout)
        box_layout.size_hint = (None, None)

        # Bind the size of the box layout to the grid layout plus some padding
        grid_layout.bind(size=self.update_box_layout_size(box_layout, grid_layout))

        self.content = box_layout

    def update_box_layout_size(self, box_layout, grid_layout):
        def _update(instance, value):
            box_layout.width = grid_layout.width + 20
            box_layout.height = grid_layout.height + 20
        return _update

    def on_image_click(self, instance):
        UsersFunc.set_profile_picture(CurrentUser().current_user.user_id, instance.background_normal)
        MDApp.get_running_app().reload_current_user()
        self.dismiss()
        show_snackbar("Profile Picture Updated")

def open_profile_picture_popup(d=None):
    popup = profile_picture_popup()
    popup.open()


class SupportPopup(Popup):  # custom pop-up widget for when creating a response
    def __init__(self, submit_callback, **kwargs):
        super(SupportPopup, self).__init__(**kwargs)
        self.title = "Ask Question"
        self.size_hint = (None, None)
        self.size = (400, 500)  # Adjust the size as needed

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Create the TextInput widget with the appropriate text
        self.support_input = TextInput(text='Issue: ', multiline=True, size_hint=(1, 5))
        self.layout.add_widget(self.support_input)

        button_layout = BoxLayout(size_hint=(1, 1), spacing=10)

        self.submit_button = Button(text="Submit", size_hint=(0.3, 1))
        self.submit_button.bind(on_press=self.submit_response)
        button_layout.add_widget(self.submit_button)

        self.close_button = Button(text="Close", size_hint=(0.3, 1))
        self.close_button.bind(on_press=self.dismiss)
        button_layout.add_widget(self.close_button)

        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

        self.submit_callback = submit_callback


    def submit_response(self, instance):  # when response is submitted
        show_snackbar("Your query has been submitted.")
        support_text = self.support_input.text
        self.submit_callback(support_text)

        self.dismiss()


class AdminSupportPopup(Popup):  # custom pop-up widget for when creating a response
    def __init__(self, submit_callback, **kwargs):
        super(AdminSupportPopup, self).__init__(**kwargs)
        self.title = "Reply"
        self.size_hint = (None, None)
        self.size = (400, 500)  # Adjust the size as needed

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.mobile = TextInput(hint_text='Mobile phone: ', multiline=True, size_hint=(1, 0.8))
        self.layout.add_widget(self.mobile)

        self.email = TextInput(hint_text='Email: *Mandatory', multiline=True, size_hint=(1, 0.8))
        self.layout.add_widget(self.email)

        # Create the TextInput widget with the appropriate text
        self.support_input = TextInput(text='Answer: ', multiline=True, size_hint=(1, 5))
        self.layout.add_widget(self.support_input)

        button_layout = BoxLayout(size_hint=(1, 1), spacing=10)

        self.submit_button = Button(text="Submit", size_hint=(0.3, 1))
        self.submit_button.bind(on_press=self.submit_response)
        button_layout.add_widget(self.submit_button)

        self.close_button = Button(text="Close", size_hint=(0.3, 1))
        self.close_button.bind(on_press=self.dismiss)
        button_layout.add_widget(self.close_button)

        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

        self.submit_callback = submit_callback

    def submit_response(self, instance):  # when response is submitted
        if self.check_in_database():
            show_snackbar("Your answer has been submitted.")
            email_text = self.email.text
            phone_text = self.mobile.text
            support_text = self.support_input.text

            self.submit_callback(phone_text, email_text, support_text)

            self.dismiss()

        else:
            show_snackbar("Email address does not exist in database.")

    def check_in_database(self):
        session = Session
        email = self.email.text
        # Check input email or mobile phone matches with the data in db
        user = session.query(CustomerSupport).filter(CustomerSupport.Email == email).first()
        session.close()
        return user is not None