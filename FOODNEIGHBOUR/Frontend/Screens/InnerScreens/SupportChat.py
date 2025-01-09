from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel

from Backend.Class.CurrentUser import CurrentUser
from Backend.Class.CustomerSupport import CustomerSupport

from Frontend.CustomTools.CustomWidgets import CustomScreen
from Frontend.CustomTools.UserWidgets import SupportPopup
from Frontend.Screens.InnerScreens.HomeForm import create_support_form

from sqlalchemy import or_
from Main import Session


class SupportChatScreen(CustomScreen):

    # Inherited Methods
    def __init__(self, **kwargs):
        super(SupportChatScreen, self).__init__(**kwargs)
        self.app.custom_screens['SupportChat'] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = False

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def clear_screen(self):
        super().clear_screen()

    # Filter the requests based on email OR phone number
    def fetch_support_requests(self):
        session = Session()
        current_user_email = CurrentUser().current_user.user_email  # Get the current user's email
        current_user_phone = CurrentUser().current_user.user_mobile # Get current user's contact number
        support_requests = session.query(CustomerSupport)\
            .filter(or_(CustomerSupport.Email == current_user_email, CustomerSupport.Contact_Us == current_user_phone))\
            .all()
        session.close()
        return support_requests

    def build_screen(self):
        super().build_screen()

        # Fetch the support requests data
        support_requests = self.fetch_support_requests()

        # Create a ScrollView
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        # Create a GridLayout for displaying the support requests
        grid_layout = GridLayout(cols=1, padding=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Create a layout for the icon button
        refresh_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))

        # Add spacer to position refresh icon
        refresh_layout.add_widget(BoxLayout(size_hint_x=8.0))

        # Add the icon button
        refresh_button = MDIconButton(icon="refresh", size_hint=(None, None), size=(dp(40), dp(40)), halign='right')
        refresh_button.bind(on_press=self.refresh_screen)
        refresh_layout.add_widget(refresh_button)

        # Add spacer
        refresh_layout.add_widget(BoxLayout())

        # Add refresh layout to the grid_layout
        grid_layout.add_widget(refresh_layout)

        support_chat_label = MDLabel(text='Chat', halign='center', height=40, size_hint_y=None)
        grid_layout.add_widget(support_chat_label)

        # Add each support request to the GridLayout as a BoxLayout
        for request in support_requests:
            box_layout = BoxLayout(orientation='vertical', padding=dp(10), size_hint_y=None, height=dp(70))

            # Add widgets to the box_layout
            issue_description_label = MDLabel(text=f'{request.Issue_Description}', font_style='Body1')

            # Check if "Answer" is in the description
            if request.Issue_Description.startswith("Answer:"):
                issue_description_label.bold = True # Bold text answer from admin
                issue_description_label.halign = 'right'

            box_layout.add_widget(issue_description_label)

            # Add the box_layout to the grid_layout
            grid_layout.add_widget(box_layout)

        # Reply user button
        if any(request.Issue_Description for request in support_requests):
            reply_user_button = MDRaisedButton(text="Reply")
            reply_user_button.bind(on_release=self.support_button_press)

            # Create new layout to center the button
            button_layout = AnchorLayout(size_hint_y=None, height=dp(60))
            button_layout.add_widget(reply_user_button)

            # Add button layout grid_layout
            grid_layout.add_widget(button_layout)

        # Add label when there is no chat history
        else:
            text_label = MDLabel(text="No chat history", size_hint_y=None,
                                  height=70, halign='center', theme_text_color='Custom', text_color=(0.5,0.5,0.5,1))
            grid_layout.add_widget(text_label)

        # Add the grid_layout to the scroll_view
        scroll_view.add_widget(grid_layout)

        # Add the scroll_view to the main layout
        self.main_space.add_widget(scroll_view)

    def refresh_screen(self, instance):
        self.clear_screen()  # Clear the current screen
        self.build_screen()  # Rebuild the screen

    def support_button_press(self, instance):  # when the comment button is pressed open popup
        support_popup = SupportPopup(submit_callback=self.handle_response_submit)
        support_popup.open()

    def handle_response_submit(self, support_input):
        print("Submitted comment:", support_input)
        create_support_form(CurrentUser().current_user.user_mobile, CurrentUser().current_user.user_email, support_input)
