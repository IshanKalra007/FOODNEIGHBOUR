from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.image import Image

import Backend.Functions.UsersFunc as UsersFunc
from Backend.Class.CurrentUser import CurrentUser
import Backend.Functions.FriendshipFunc as FriendshipFunc
from Frontend.CustomTools.AdvertWidgets import AdvertSearchResultsWidget
from Frontend.CustomTools.CustomWidgets import CustomScreen, label_helper_1, link_button_helper
from functools import partial

buttons_helper = """
FloatLayout:
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x' : 0.5, 'center_y': 0.5}
        on_release:
            app.custom_screens["Login"].submit_login_details()
    MDFlatButton:
        text: "Don't have an account? Sign up..."
        pos_hint: {'center_x' : 0.5, 'center_y': 0.1}
        on_release: app.change_outer_screen('register_details')
        theme_text_color: "Custom"
        text_color: app.link_color
    
    MDRectangleFlatButton:
        text: 'DebugFill'
        pos_hint: {'center_x' : 0.5, 'center_y': 0.4}
        on_release:
            app.custom_screens["Login"].debug_fill_details()
"""


class ProfileScreen(CustomScreen):
    # Inherited Methods
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.profile_id = ''
        self.app.custom_screens["Profile"] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = True
        self.scrollable = True

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def build_screen(self):
        if not super().build_screen():
            return False

        total_height = 5
        spacing = 6

        self.current_user = CurrentUser().current_user  # calls current user
        self.profile_user = UsersFunc.get_user(self.profile_id)  # finds the user with the profile we are looking at
        # if these are the same then the current user is the profile owner
        is_current_users = self.profile_user.user_id == self.current_user.user_id

        # Create a layout to hold the content of the profile screen
        content_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=spacing)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        if is_current_users:
            imagepath = self.current_user.imagepath
        else:
            imagepath = self.profile_user.imagepath

        user_image = Image(source=imagepath, size_hint=(None, None), height=dp(100), pos_hint={'center_x': 0.5})
        content_layout.add_widget(user_image)

        # Populate the text fields with user data
        user_name = Builder.load_string(label_helper_1)
        user_name.font_size = 25
        user_name.text = self.profile_user.user_name
        content_layout.add_widget(user_name)

        if not is_current_users:
            self.follow_button = MDRectangleFlatButton(text="Follow", pos_hint={'center_x': 0.5},
                                                       on_release=self.toggle_follow)
            content_layout.add_widget(self.follow_button)
            if FriendshipFunc.check_friendship_exists(user_id=self.current_user.user_id, friend_id=self.profile_id):
                self.follow_button.text = "Unfollow"

            total_height += self.follow_button.height + spacing

        # Create a horizontal layout for followers and flags
        followers_flags_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), padding=10)

        self.followers_label = MDLabel(text="Friends: " + str(UsersFunc.count_friends(self.profile_user.user_id)),
                                       halign='left', size_hint_x=None, width=dp(100), font_size=25)
        self.followers_label.bind(size=self.followers_label.setter('text_size'))
        followers_flags_layout.add_widget(self.followers_label)

        self.flags_label = MDLabel(text="Flags: " + str(self.profile_user.user_flag_counter),
                                   halign='right', size_hint_x=None, width=dp(100), font_size=25)
        self.flags_label.bind(size=self.flags_label.setter('text_size'))
        followers_flags_layout.add_widget(self.flags_label)

        # Center the followers_flags_layout
        followers_flags_layout.size_hint_x = None
        followers_flags_layout.width = self.flags_label.width + self.followers_label.width + dp(10)
        followers_flags_layout.pos_hint = {'center_x': 0.5}

        # Add the followers and flags layout to the content layout
        content_layout.add_widget(followers_flags_layout)

        total_height += user_image.height + user_name.height + followers_flags_layout.height + (spacing * 3)

        if is_current_users:
            private_details_spacing = 50

            private_info_heading = Builder.load_string(label_helper_1)
            private_info_heading.font_size = 15
            private_info_heading.text = "Your information (private):"
            content_layout.add_widget(private_info_heading)

            user_email = Builder.load_string(label_helper_1)
            user_email.text = "EMAIL: \n" + self.profile_user.user_email
            user_email.height = dp(private_details_spacing)
            content_layout.add_widget(user_email)

            user_mobile = Builder.load_string(label_helper_1)
            user_mobile.text = "PHONE NUMBER: \n" + self.profile_user.user_mobile
            user_mobile.height = dp(private_details_spacing)
            content_layout.add_widget(user_mobile)

            post_code = Builder.load_string(label_helper_1)
            post_code.text = "POSTCODE: \n" + self.profile_user.user_postcode
            post_code.height = dp(private_details_spacing)
            content_layout.add_widget(post_code)

            edit_details_button = Builder.load_string(link_button_helper)
            edit_details_button.text = 'Edit details or change password'
            edit_details_button.font_size = 13
            edit_details_button.on_release = partial(self.app.change_inner_screen, 'edit_details')
            content_layout.add_widget(edit_details_button)

            total_height += (private_info_heading.height + user_email.height + user_mobile.height + post_code.height +
                             edit_details_button.height + (spacing * 4))

        # Add a label for the advertisement section
        advertisement_label = MDLabel(
            text="  " + ("Your" if is_current_users else self.profile_user.user_name + "'s") + " posts:",
            size_hint=(1, None),
            height=dp(48),  # Adjust the height as needed
            color=(1, 0, 0, 1)  # Red color for debugging
        )
        content_layout.add_widget(advertisement_label)
        total_height += advertisement_label.height + spacing

        # Add the results widget
        self.results_widget = AdvertSearchResultsWidget(self.app, auto_make_search=False, lock_scroll=True,
                                                        results_per_page=5, allow_deletion=True,
                                                        user_id_filter=self.profile_id)
        self.results_widget.make_search('', user_id_filter=self.profile_id)
        content_layout.add_widget(self.results_widget.scroll_port)
        total_height += self.results_widget.scroll_port.height

        content_layout.height = total_height
        self.scroll_space.height = total_height

        # Add the content layout to the scroll_view in main_space
        self.scroll_space.add_widget(content_layout)

        return True

    def clear_screen(self):
        del self.results_widget
        self.current_user = None
        self.profile_user = None
        super().clear_screen()

    def toggle_follow(self, d=None):
        if self.current_user is not None and self.profile_user is not None:
            if FriendshipFunc.check_friendship_exists(user_id=self.current_user.user_id, friend_id=self.profile_id):
                self.follow_button.text = "Follow"
                FriendshipFunc.delete_friend(self.current_user.user_id, self.profile_user.user_id)
            else:
                self.follow_button.text = "Unfollow"
                FriendshipFunc.add_friend(self.current_user.user_id, self.profile_user.user_id)
            self.update_stats_count()

    def update_stats_count(self):
        friend_count = UsersFunc.count_friends(self.profile_user.user_id)
        self.followers_label.text = "Friends: " + str(friend_count)
        self.flags_label.text = "Flags: " + str(self.profile_user.user_flag_counter)
