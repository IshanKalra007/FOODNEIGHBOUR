from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget
from kivy.uix.boxlayout import BoxLayout
from Backend.Class.CurrentAdvert import CurrentAdvert
from Backend.Class.CurrentUser import CurrentUser
from Backend.Functions.AdvertFunc import determine_location
from Backend.Functions.ResponseFunc import (create_response, query_response, bookmark_advert, check_is_bookmarked,
                                            remove_bookmark)
from Backend.Functions.UsersFunc import report_user, get_user

from Frontend.CustomTools.CustomWidgets import CustomScreen, get_location_from_coords, generate_label, show_snackbar
from Frontend.CustomTools.UserWidgets import ResponsePopup
from Frontend.CustomTools.AdvertWidgets import DeleteAdvertDialogue

from functools import partial

ad_image_helper = '''
MDFloatLayout:
    pos_hint_y: None
    pos_hint_x: 0
    size_hint: (1, None)
    height: 140
    md_bg_color: app.theme_cls.primary_color
    Image:
        source: 'Images/placeholderFoodPic.jpg'
        size_hint: (1, 1)
        size: self.parent.size
        pos: self.parent.pos
        allow_stretch: True  # Allow stretching the image to fill the button
        keep_ratio: True
    MDLabel:
        id:type_label
        text: "Donation"
        color: "white"
        pos_hint: {'center_x' : 0.2, 'center_y' : 0.9}
        size_hint: (0.4,None)
        height: 30
        halign: 'left'
        valign: 'top'
        md_bg_color:(0.09, 0.63, 0.5, 1)
        padding: (4, 100)
    MDLabel:
        id:title_label
        text: " Food Product 0"
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.1}
        size_hint: (1,None)
        height: 30
        font_style:"H6"
        halign: 'left'
        valign: 'bottom'
        md_bg_color: (1,1,1, 0.5)
        padding: (4, 100)
    MDIconButton:
        id:delete_button
        icon: 'delete'
        size: (80,80)
        color: (0,0,0,0)
        pos_hint: {'center_x' : 0.92, 'center_y' : 0.9}
        theme_icon_color: "Custom"
        icon_color: (1,1,1,1)
'''

icon_bar_helper = '''
MDBoxLayout:
    orientation: 'vertical'
    size_hint: (1, None)
    height:30
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 50
        Widget:
            size_hint_x: 1 
        Button:
            id:profile_button
            size_hint: None, None
            size: dp(35), dp(40)
            color: (0,0,0,0)
            background_normal: ''  # Remove the default background
            background_down: ''  # Remove the default pressed background
            background_color: (1, 1, 1, 0)  # Transparent background
            border: (0, 0, 0, 0)  # No border
            Image:
                id: prof_pic
                source:''
                size_hint: (None,None)
                pos_hint: (None,None)
                size: self.parent.size
                pos: self.parent.pos
        MDLabel:
            id:user_label
            text:"User"
            size_hint: None, None
            size: dp(120), dp(40)
        MDIconButton:
            icon: 'comment-outline'
            size_hint: None, None
            size: dp(35), dp(40)
            on_press: app.custom_screens["AdvertView"].response_button_press()
        MDIconButton:
            id: bookmark_button
            icon: 'bookmark'
            size_hint: None, None
            size: dp(35), dp(40)
            theme_icon_color: "Primary"
            icon_color: app.theme_cls.primary_color
            on_press: app.custom_screens["AdvertView"].bookmark_button_press()
        MDIconButton:
            id: flag_button
            icon: 'flag-outline'
            size_hint: None, None
            size: dp(35), dp(40)
            on_press: app.custom_screens["AdvertView"].report_button_press()

'''


class AdvertViewScreen(CustomScreen):

    def __init__(self, **kwargs):
        super(AdvertViewScreen, self).__init__(**kwargs)
        self.app.custom_screens["AdvertView"] = self
        self.rebuild_on_load = True
        self.top_seq_y = 0.9
        self.has_back_button = False

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def build_screen(self):
        if not super().build_screen():
            return False

        current_advert = CurrentAdvert().current_advert
        poster_user = get_user(current_advert.user_id)
        current_user = CurrentUser().current_user
        determine_location(current_advert, current_user.location)

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_y=True)
        self.main_space.add_widget(scroll_view)

        advert_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=0, spacing=15)
        advert_layout.bind(minimum_height=advert_layout.setter('height'))

        # Advert image (Currently a placeholder)
        ad_image = Builder.load_string(ad_image_helper)
        ad_image.ids.type_label.text = current_advert.advert_type
        ad_image.ids.title_label.text = " " + current_advert.advert_name
        # only delete if your post or admin
        if current_advert.user_id == current_user.user_id or current_user.user_type == "ADMIN":
            ad_image.ids.delete_button.on_release = partial(self.delete_button_press, current_advert.advert_id)
        else:
            ad_image.ids.delete_button.disabled = True
            ad_image.ids.delete_button.opacity = 0
        advert_layout.add_widget(ad_image)

        # Icon bar (profile button, username, comment, bookmark, flag)
        icon_bar = Builder.load_string(icon_bar_helper)
        icon_bar.ids.user_label.text = " " + poster_user.user_name
        icon_bar.ids.prof_pic.source = poster_user.imagepath
        icon_bar.ids.profile_button.on_release = partial(self.app.go_to_profile_screen, str(poster_user.user_id))
        # Set bookmarked representation
        self.bookmark_button = icon_bar.ids.bookmark_button
        is_bookmarked = check_is_bookmarked(current_advert.advert_id, CurrentUser().current_user.user_id)
        self.bookmark_button.theme_icon_color = "Custom" if is_bookmarked else "Primary"
        self.flag_button = icon_bar.ids.flag_button

        advert_layout.add_widget(icon_bar)

        advert_layout.add_widget(generate_label(current_advert.advert_description, height=50))
        advert_layout.add_widget(generate_label(str(round(current_advert.distance * 10) / 10) + " miles away"))

        location = get_location_from_coords(current_advert.location_coords)
        if location is not None:
            address = location.address
        else:
            address = "FAILED TO LOAD ADDRESS"

        advert_layout.add_widget(generate_label("Pickup Time: \n" + str(current_advert.advert_time)))

        advert_layout.add_widget(generate_label("Location: \n" + address, height=100))
        advert_layout.add_widget(generate_label("Mobile: \n" + poster_user.user_mobile))

        # Query responses for the current advert
        responses = query_response(current_advert.advert_id)
        # Add responses to the list
        item_list = MDList()
        for user, response in responses:
            if not response.bookmarked:
                user_name_str = str(user.user_name)
                response_content_str = str(response.response_content)
                imagepath_str = str(user.imagepath)

                # Create a TwoLineAvatarListItem with the ImageLeftWidget
                item = TwoLineAvatarListItem(
                    text=user_name_str,
                    secondary_text=response_content_str,
                )

                # Create an ImageLeftWidget with the avatar image
                image_widget = ImageLeftWidget(source=imagepath_str)
                item.add_widget(image_widget)

                item_list.add_widget(item)
        advert_layout.add_widget(item_list)  # Add the MDList to the advert_layout

        scroll_view.add_widget(advert_layout)

        return True

    def clear_screen(self):
        super().clear_screen()

    def report_button_press(self):
        current_advert = CurrentAdvert().current_advert
        report_user(current_advert.advert_id)
        show_snackbar("User Reported Successfully")
        self.flag_button.disabled = True

    def response_button_press(self):  # when the comment button is pressed open popup
        response_popup = ResponsePopup(submit_callback=self.handle_response_submit)
        response_popup.open()

    def bookmark_button_press(self):
        is_bookmarked = check_is_bookmarked(CurrentAdvert().current_advert.advert_id,
                                            CurrentUser().current_user.user_id)
        print("is bookmarked " + str(is_bookmarked))
        if not is_bookmarked:
            bookmark_advert(CurrentAdvert().current_advert.advert_id, CurrentUser().current_user.user_id)
        else:
            remove_bookmark(CurrentAdvert().current_advert.advert_id, CurrentUser().current_user.user_id)
        self.bookmark_button.theme_icon_color = "Primary" if is_bookmarked else "Custom"

    def handle_response_submit(self, comment_text):  # here the comment_text will be added as a response
        print("Submitted comment:", comment_text)
        create_response(CurrentUser().current_user.user_id, CurrentAdvert().current_advert.advert_id, comment_text)
        self.refresh_screen()

    def delete_button_press(self, advert_id, d=None):
        delete_dialogue = DeleteAdvertDialogue(advert_id)
        # Leave the page if the user confirms post deletion
        delete_dialogue.on_confirm_actions.append(self.app.go_back)
