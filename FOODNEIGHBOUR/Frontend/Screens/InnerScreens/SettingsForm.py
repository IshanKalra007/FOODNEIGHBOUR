from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from Frontend.CustomTools.CustomWidgets import CustomScreen, LocationPicker, generate_label
from Backend.Class.CurrentUser import CurrentUser
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from functools import partial

setting_helper = """
MDFloatLayout:
    size_hint:(None,None)
    size:(300,50)
    MDLabel:
        id: label
        text: "Setting"
        size_hint:(None,1)
        width:235
        halign: "left"
        pos_hint:{'center_x':0.42,'center_y':0.5}
    MDSwitch:
        pos_hint:{'center_x':0.85,'center_y':0.4}
"""


class SettingsScreen(CustomScreen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.app.custom_screens['Settings'] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = False
        self.scrollable = True

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def clear_screen(self):
        super().clear_screen()

    def build_screen(self):
        super().build_screen()

        # Create a scroll view to hold the content if needed
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_y=True)
        self.main_space.add_widget(scroll_view)

        settings_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=20)
        settings_layout.bind(minimum_height=settings_layout.setter('height'))

        # Add title label
        settings_layout.add_widget(generate_label("Settings", font_style="H6", height=30))

        self.location_picker = LocationPicker(CurrentUser().current_user.location)
        settings_layout.add_widget(self.location_picker.location_field.text_field)

        # Add the main button that triggers the popup
        popup_button = MDRaisedButton(text="Edit Account Details", size_hint=(None, None),height=60,
                                      width=dp(250), pos_hint={'center_x':0.5})
        popup_button.bind(on_release=partial(self.app.change_inner_screen, 'edit_details'))
        settings_layout.add_widget(popup_button)

        settings_layout.add_widget(generate_label(""))
        # Add title label
        settings_layout.add_widget(generate_label("Notifications", font_style="H6"))
        settings_layout.add_widget(generate_label("(in development)"))

        # Add labels and switches for notification settings
        labels = ["New advertisements from followed Accounts", "New advertisements from nearby location",
                  "Pickup reminder"]
        for label_text in labels:
            # Add label and switch to box layout
            floater_setting = Builder.load_string(setting_helper)
            floater_setting.ids.label.text = label_text
            settings_layout.add_widget(floater_setting)

        # Add title label
        settings_layout.add_widget(generate_label("Email Preferences", font_style="H6"))
        settings_layout.add_widget(generate_label("(in development)"))

        # Add labels and switches for notification settings
        labels = ["Daily Updates ", "Weekly Email ", "Monthly Digest "]
        for label_text in labels:
            # Add label and switch to grid layout
            floater_setting = Builder.load_string(setting_helper)
            floater_setting.ids.label.text=label_text
            settings_layout.add_widget(floater_setting)

        scroll_view.add_widget(settings_layout)

    def on_point_three_update(self, run_time):
        super().on_point_three_update(run_time)
        if self.is_built and self.location_picker is not None:
            self.location_picker.on_point_three_update(run_time)
