from kivy.lang import Builder

from Backend.Class.CurrentUser import CurrentUser
from Backend.Class.CustomerSupport import CustomerSupport

from Frontend.CustomTools.CustomWidgets import CustomScreen
from Frontend.CustomTools.UserWidgets import SupportPopup
from Frontend.CustomTools.AdvertWidgets import AdvertSearchResultsWidget, search_bar_helper

from Main import Session

support_chat_button_helper = """
FloatLayout: 
    MDFloatingActionButton:
        icon: "chat-question"
        pos_hint: {'center_x': 0.9, 'center_y': 0.1}
        on_release:
            app.custom_screens["Home"].support_button_press()
"""


class HomeScreen(CustomScreen):

    # Inherited Methods
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.search_field = None
        self.app.custom_screens["Home"] = self  # so this instance can be accessed via app.login_screen
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = False

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def build_screen(self):
        if not (super().build_screen()): return False

        # Search bar
        search_bar = Builder.load_string(search_bar_helper)
        self.main_space.add_widget(search_bar)

        # Advert results
        self.results_widget = AdvertSearchResultsWidget(self.app, search_bar,results_per_page=5)
        self.main_space.add_widget(self.results_widget.scroll_port)

        # Chat support button
        support_chat_button = Builder.load_string(support_chat_button_helper)
        self.main_space.add_widget(support_chat_button)

        return True

    def clear_screen(self):
        super().clear_screen()

    def on_point_three_update(self, run_time):
        super().on_point_three_update(run_time)
        if (self.is_built):
            self.results_widget.on_point_three_update(run_time) #Call update on advert results view

    # Local Methods
    def support_button_press(self):  # when the comment button is pressed open popup
        support_popup = SupportPopup(submit_callback=self.handle_response_submit)
        support_popup.open()

    def handle_response_submit(self, support_input):  # here the comment_text will be added as a response
        print("Submitted comment:", support_input)
        create_support_form(CurrentUser().current_user.user_mobile, CurrentUser().current_user.user_email, support_input)


def create_support_form(contact_us, email, issue_description):
    session = Session()
    new_support_form = CustomerSupport(
        contact_us=contact_us,
        email=email,
        issue_description=issue_description
    )
    session.add(new_support_form)
    session.commit()
    session.close()




    
