from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from Backend.Class.CurrentAdvert import CurrentAdvert
from Backend.Class.CurrentUser import CurrentUser
from Backend.Functions.UsersFunc import get_user
from Frontend import MainHelper
from kivy.clock import Clock
import time
from functools import partial

Window.size = (300, 500)  # Just for development
Window.minimum_width, Window.minimum_height = (300, 500)


class FoodShareApp(MDApp):
    def __init__(self, **kwargs):
        super(FoodShareApp, self).__init__(**kwargs)
        self.custom_screens = {}
        self.is_in_inner = False
        self.val_fields = []
        self.start_time = time.time()

    def on_start(self):
        # Call update every 0.3seconds
        Clock.schedule_interval(self.point_three_update, 0.3)

    def build(self):
        # Set theme
        self.theme_cls.primary_palette = 'Blue'
        self.link_color = (0.2, 0.6, 1, 1)
        # Build the screen
        root_screen = Builder.load_string(MainHelper.main_helper)
        return root_screen

    # Close or open the navigation draw
    def navigation_draw(self, state):
        self.root.ids.nav_drawer.set_state(state)

    # Navigate to a specified inner screen (logged in screens)
    def change_inner_screen(self, screen, d=None):
        self.navigation_draw('closed')

        # Customise toolbar depending on what screen its on
        if screen == 'home':
            self.root.ids.inner_screen.ids.toolbar.right_action_items[0] = ["plus",
                                                                            partial(self.change_inner_screen,
                                                                                    'post_advert')]
            self.root.ids.inner_screen.ids.toolbar.title = "Advert Feed"
        else:
            self.root.ids.inner_screen.ids.toolbar.right_action_items[0] = ["home",
                                                                            partial(self.change_inner_screen,
                                                                                    'home')]
            self.root.ids.inner_screen.ids.toolbar.title = ""

        self.root.ids.inner_screen.ids.inner_screen_manager.current = screen

    # Navigate to a specified outer screen (logged out screens)
    def change_outer_screen(self, screen):
        self.navigation_draw('closed')

        if screen == 'inner_screen':
            self.change_inner_screen('home')  # revert to homepage when opening inner screen/logging in
            self.is_in_inner = True
        else:
            self.is_in_inner = False

        self.root.ids.outer_screen_manager.current = screen

    # Navigate to the profile screen of a specified user
    def go_to_profile_screen(self, profile_id):
        if profile_id == 'current_user': profile_id = str(CurrentUser().current_user.user_id)
        self.custom_screens['Profile'].profile_id = profile_id
        self.change_inner_screen('profile')

    # Navigate to the advert view screen of a specified advert
    def open_advert_view(self, advert):
        CurrentAdvert().current_advert = advert
        self.change_inner_screen('advert_view')

    # Revert to home screen of respective current inner/outer space
    def go_back(self):
        if self.is_in_inner:
            self.change_inner_screen('home')
        else:
            self.change_outer_screen('outer_home')

    # Root regular update called every 0.3 seconds
    def point_three_update(self, event):
        run_time = time.time() - self.start_time

        # Cascades update to all screens linked
        for cs_key in self.custom_screens:
            self.custom_screens[cs_key].on_point_three_update(run_time)

    # Reload the details of the current user
    def reload_current_user(self):
        CurrentUser().current_user = get_user(CurrentUser().current_user.user_id)
        self.update_nav_bar_details()

    # Update all details in navbar e.g: profile picture and emails to that of whats loaded
    def update_nav_bar_details(self):
        current_user = CurrentUser().current_user
        self.root.ids.profile_picture.source = current_user.imagepath
        self.root.ids.username_label.text = current_user.user_name
        self.root.ids.email_label.text = current_user.user_email
        if current_user.user_type != 'ADMIN':  # Disable admin button
            self.root.ids.admin_button.disabled = True
            self.root.ids.admin_button.opacity = 0
        else:
            self.root.ids.admin_button.disabled = False  # Enable admin button
            self.root.ids.admin_button.opacity = 1

        # Always show support button for showcase purposes
        # if current_user.user_type != 'USER':  # Disable support button
        #     self.root.ids.support_button.disabled = True
        #     self.root.ids.support_button.opacity = 0
        # else:
        #     self.root.ids.support_button.disabled = False # Enable support button
        #     self.root.ids.support_button.opacity = 1


if __name__ == "__main__":
    FoodShareApp().run()
