from kivy.lang import Builder
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from functools import partial
from kivy.clock import Clock

from Frontend.CustomTools.CustomWidgets import ValidationField, generate_dropdown, user_data_field_helper, \
    show_snackbar, LocationPicker
from Backend.Class.CurrentUser import CurrentUser
from Backend.Functions.AdvertFunc import HomePageAdvertQuery, HomePageSearch, sort_and_filter, delete_advert
from kivymd.uix.dialog import MDDialog

adverts_view_helper = """
#:import ScrollEffect  kivy.effects.scroll.ScrollEffect
ScrollView:
    effect_y: ScrollEffect() #To prevent default bouncy dampening effect
    always_overscroll: True
    do_scroll_x: False
    overscroll:0
    size_hint: (0.95,1)
    pos_hint: {'center_x' : 0.5}
    pos_hint_y: None
    pos: (0, -40)
"""
adverts_layout_helper = """
FloatLayout:
        id: sec_layout
        padding: 8
        size_hint_y: None  # this is required for scrolling
        height: 1000
"""

advert_helper = """
MDFloatLayout:
    pos_hint_y: None
    pos_hint_x: 0
    size_hint: (1, None)
    height: 140
    md_bg_color: app.theme_cls.primary_color
    Button:
        id:thumbnail_button
        size_hint: (0.98,0.98)
        size: (30,30)
        color: 0.13, 0.58, 0.95, 1
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.5}
        on_release: app.open_advert_view(root.advert)
        background_color: 0.13, 0.58, 0.95, 0  # Blue color for the button background
        Image:
            source: 'Images/placeholderFoodPic.jpg'
            size_hint: (None, None)
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
        id:title_details
        text: " Food Product 0"
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.18}
        size_hint: (1,None)
        height: 60
        halign: 'left'
        valign: 'bottom'
        md_bg_color: (1,1,1, 0.5)
        padding: (4, 100)

    Button:
        id:profile_button
        size_hint: (None,None)
        size: (50,50)
        color: (0,0,0,0)
        pos_hint: {'center_x' : 0.93, 'center_y' : 0.87}
        background_normal: ''  # Remove the default background
        background_down: ''  # Remove the default pressed background
        background_color: (1, 1, 1, 0)  # Transparent background
        border: (0, 0, 0, 0)  # No border
        
        Image:
            id: profile_image
            source: '' # for each of these images it needs to be its retrospective user profile image
            size_hint: (None,None)
            pos_hint: (None,None)
            size: self.parent.size
            pos: self.parent.pos
    MDIconButton:
        id:delete_button
        icon: 'delete'
        size: (80,80)
        color: (0,0,0,0)
        pos_hint: {'center_x' : 0.92, 'center_y' : 0.17}
        theme_icon_color: "Custom"
        icon_color: (1,1,1,1)
"""

search_bar_helper = """
BoxLayout:
    orientation: 'horizontal' 
    size_hint: (0.5, 0.1)
    pos_hint: {'center_x': 0.25, 'center_y': 0.93}
    MDIconButton:
        icon: 'refresh'
        pos_hint: {'center_y': 0.7}
        padding: 15
    MDTextField:
        hint_text: "Search"
        helper_text: ""
        #icon_right_color: app.theme_cls.primary_color
        helper_text_mode: "on_focus"
        #pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x:None
        width:160
    MDIconButton:
        icon: 'filter'
        pos_hint: {'center_y': 0.7}
        padding: 10
        theme_icon_color: "Primary"
        icon_color: app.theme_cls.primary_color
    MDIconButton:
        icon: 'bookmark'
        pos_hint: {'center_y': 0.7}
        padding: 10
        theme_icon_color: "Primary"
        icon_color: app.theme_cls.primary_color
"""


class AdvertSearchResultsWidget():
    def __init__(self, app, search_bar=None, lock_scroll=False,
                 results_per_page=10, allow_deletion=False, user_id_filter='', auto_make_search=False):
        self.app = app
        self.scroll_content = Builder.load_string(adverts_layout_helper)
        self.scroll_port = self.scroll_content
        if not lock_scroll:
            self.scroll_port = Builder.load_string(adverts_view_helper)
            self.scroll_port.add_widget(self.scroll_content)
        else:
            self.scroll_content.height = 1000
        self.results_per_page = results_per_page
        self.page_count = 0
        self.cur_page = 0
        self.results = []
        self.page_results = []
        self.search_string = ''
        self.filter_dialog = None
        self.allow_deletion = allow_deletion
        self.bookmarked_only = False
        self.custom_filters = False
        self.filter_button = None
        self.user_id_filter = user_id_filter
        self.reset_filters()

        self.make_gen_search()
        self.search_field = None
        self.location_picker = None
        if search_bar is not None:
            self.search_field = ValidationField(
                text_field_widget=search_bar.children[2],
                label="Search", validation_check="", required=False)
            self.refresh_button = search_bar.children[3]
            self.refresh_button.on_release = self.refresh_results
            self.filter_button = search_bar.children[1]
            self.filter_button.on_release = self.open_filter_dialog
            self.bookmarks_button = search_bar.children[0]
            self.bookmarks_button.on_release = self.toggle_bookmarked_only

        if lock_scroll:
            self.scroll_content.size_hint = (0.95, None)
            self.scroll_content.height = 800

    def on_point_three_update(self, run_time):
        if self.search_field is not None:
            stopped_typing = self.search_field.check_for_change(run_time)
            if stopped_typing:
                self.search_string = self.search_field.text_field.text
                self.make_gen_search()
        if self.location_picker is not None:
            self.location_picker.on_point_three_update(run_time)

    def refresh_results(self, snackbar=True):
        self.clear_results()
        if snackbar:
            show_snackbar("Refreshed feed")
        Clock.schedule_once(self.make_gen_search, 0.1)

    def make_search(self, search_input='', d=None, post_type_filter='', sort_mode='', sort_order='', user_id_filter='',
                    max_dist_filter='', min_follow_count_filter=''):
        self.load_results(search_input)
        self.results = sort_and_filter(self.results, post_type=post_type_filter, sort_mode=sort_mode,
                                       sort_order=sort_order,
                                       owner_id=user_id_filter, cur_user_id=CurrentUser().current_user.user_id,
                                       max_dist_filter=max_dist_filter,
                                       min_follow_count_filter=min_follow_count_filter,
                                       bookmarked_only=self.bookmarked_only,
                                       cur_user_location=CurrentUser().current_user.location)
        self.cur_page = 0
        self.load_page()
        self.display_results()

    def make_gen_search(self, d=None):
        self.make_search(self.search_string, post_type_filter=self.post_type_filter, sort_mode=self.sort_mode,
                         sort_order=self.sort_order, user_id_filter=self.user_id_filter,
                         max_dist_filter=self.max_dist_filter, min_follow_count_filter=self.min_follows_filter)

    def load_results(self, search_string=''):
        if search_string == '':
            self.results = HomePageAdvertQuery()
        else:
            self.results = HomePageSearch(search_string)

    def load_page(self, page_index=0):
        # current_pages_rows = adverts.limit(10).offset(page_number * 10).all()
        # query 10 adverts per page, takes page_number as a parameter
        i = 0
        self.page_count = 0
        self.page_results = []
        for advert, user in self.results:
            if self.page_count == 0:
                self.page_count = 1
            if i // self.results_per_page == page_index:
                self.page_results.append([advert, user])
            if i % self.results_per_page == 0 and i > 0:
                self.page_count += 1
            i += 1

    def clear_results(self):  # Removes all children in the scroll_content
        while len(self.scroll_content.children) > 0:
            self.scroll_content.remove_widget(self.scroll_content.children[0])

    def display_results(self):
        self.scroll_port.scroll_y = 1  # Set scroll view back to top
        self.clear_results()  # Reset scroll_content

        i = 0
        spacing = 140 + 5  # height of advert widget + padding
        y_offset = 0
        y_extension = 0
        current_user = CurrentUser().current_user

        if self.page_count > 0:  # There are results to show, display them

            show_page_buttons = self.page_count > 0
            top_button_line = None
            if show_page_buttons:
                y_extension += 30
                if self.cur_page != 0:  # Do not display top page buttons on page 0
                    top_button_line = self.generate_page_buttons()
                    self.scroll_content.add_widget(top_button_line)
                    y_offset += 30  # Lower everything else to make room for these buttons
            # Calculate the height of scroll_content before assigning positions that will get distorted otherwise
            self.scroll_content.height = (len(self.page_results) * spacing) + 50 + y_offset + y_extension

            final_y_pos = 0
            for result in self.page_results:
                advert = result[0]
                user = result[1]

                advert_widget = Builder.load_string(advert_helper)
                advert_widget.advert = advert  # Assign advert to the widget
                adheight = advert_widget.height
                self.scroll_content.add_widget(advert_widget)

                final_y_pos = self.scroll_content.height - adheight - (
                        spacing * i) - y_offset  # Work out the ypos of the last advert
                advert_widget.pos = (0, final_y_pos)
                # Fill in details of the advert
                advert_widget.ids.type_label.text = " " + advert.advert_type
                details_string = " " + advert.advert_name
                if advert.distance != -1: details_string += " \n " + str(
                    round(advert.distance * 10) / 10) + " miles away"

                advert_widget.ids.title_details.text = details_string
                advert_widget.ids.profile_button.on_release = partial(self.app.go_to_profile_screen,
                                                                      str(advert.user_id))
                advert_widget.ids.profile_image.source = user.imagepath  # sets the image path for each user's advert

                if advert.advert_type == "DONATION":
                    advert_widget.ids.type_label.md_bg_color = self.app.theme_cls.primary_color

                if (self.allow_deletion and (
                        # Only be able to delete your own posts OR be an admin
                        current_user.user_id == advert.user_id or current_user.user_type == "ADMIN")):
                    advert_widget.ids.delete_button.on_release = partial(self.press_delete_advert, advert.advert_id)
                    advert_widget.ids.delete_button.disabled = False
                    advert_widget.ids.delete_button.opacity = 1
                else:
                    advert_widget.ids.delete_button.disabled = True
                    advert_widget.ids.delete_button.opacity = 0

                i += 1

            if show_page_buttons:  # Generate and place page buttons at the bottom
                bottom_button_line = self.generate_page_buttons()
                bottom_button_line.pos_hint_y = None
                self.scroll_content.add_widget(bottom_button_line)
                bottom_button_line.pos = (10, final_y_pos - 40)
                if top_button_line is not None:
                    top_button_line.pos = (
                        12, self.scroll_content.height - 35)  # Finally assign the position of the top page buttons
        else:  # There are no results to show, display a message
            self.scroll_content.height = 200
            self.scroll_content.add_widget(
                MDLabel(text="No Results! ", halign='center', text_color=self.app.link_color, font_style='H4',
                        size_hint=(None, None),
                        size=(300, 100), pos=(0, 100)))
            self.scroll_content.add_widget(
                MDLabel(text="Try broadening your search terms", halign='center', text_color=self.app.link_color,
                        font_style='Body1',
                        size_hint=(None, None),
                        size=(300, 100), pos=(0, 60)))

    def generate_page_buttons(self):
        # Determine the mun page number to iterate from:
        min_page_num = max(0, self.cur_page - 1)
        # If past first 2 pages start range 2 before the current page (1st can be used for jump buttons)
        if self.cur_page > 1:
            min_page_num = self.cur_page - 2

        # Setup Layout for buttons to go in:
        buttons_line = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        # Add label:
        buttons_line.add_widget(
            MDLabel(text="Pages: ", theme_text_color='Custom', halign='left', text_color=self.app.link_color,
                    font_style='Body1', size_hint=(None, None), size=(50, 40)))
        i = 0
        # Display nums from min all the way to end or 4 pages ahead depending on which is closest
        for page_index in range(min_page_num, min(min_page_num + 5, self.page_count)):
            txt = str(page_index + 1)
            # Add 1 to index for page label since most page systems start at 1
            padding = 15
            color = self.app.link_color

            destination_page = page_index
            # Highlight the current page number with a different color
            if page_index == self.cur_page:
                color = (1, 0, 1, 1)
            # If the 1st button along and not currently on first 2 pages make this button jump to start
            if i == 0 and self.cur_page > 1:
                destination_page = 0
                txt = "...1"
                padding = 5
            # If the 5th button along and not currently on last 2 pages make this button jump to end
            if i == 4 and page_index < self.page_count - 1:
                destination_page = self.page_count - 1
                txt = "..." + str(self.page_count)
                padding = 5
            # Generate the button widget
            page_button = MDFlatButton(text=txt, theme_text_color="Custom", text_color=color,
                                       size_hint=(None, None), _min_width=15, size=(5, 5), padding=padding,
                                       # Partial is used in order to pass parameter
                                       on_release=partial(self.set_page,
                                                          destination_page))
            buttons_line.add_widget(page_button)
            i += 1
        return buttons_line

    def set_page(self, page, d=None):
        self.cur_page = page
        self.load_page(page)
        self.display_results()

    def open_filter_dialog(self):
        if self.filter_dialog is None:
            self.filter_dialog = MDDialog(title=' Search Filters', type="custom", content_cls=FilterDialogContent(),
                                          buttons=[MDFlatButton(text='Close',
                                                                on_release=self.close_filter_dialog),
                                                   MDFlatButton(text='Reset',
                                                                on_release=self.reset_filters),
                                                   MDFlatButton(text='Apply',
                                                                on_release=self.apply_filters)])
            box_layout = Builder.load_string(filter_dialog_helper)
            self.filter_dialog.content_cls.add_widget(box_layout)

            self.location_picker = LocationPicker(CurrentUser().current_user.location)
            box_layout.add_widget(self.location_picker.location_field.text_field)

            self.post_type_dropdown = generate_dropdown("Post Types:", ["All", "Requests", "Donations"], box_layout)
            self.sort_by_dropdown = generate_dropdown("sort by", ["Distance", "Time", "Most Recent"], box_layout)
            self.sort_order_dropdown = generate_dropdown("sort order", ["Ascending", "Descending"], box_layout)

            self.max_dist_field = ValidationField(text_field_widget=Builder.load_string(user_data_field_helper),
                                                  label="maximum distance",
                                                  min_text_length=1,
                                                  max_text_length=10, helper_text='(miles)')
            box_layout.add_widget(self.max_dist_field.text_field)

            # Don't add to dialog until min followers filter functionality is implemented
            self.min_follows_field = ValidationField(text_field_widget=Builder.load_string(user_data_field_helper),
                                                     label="minimum poster follow count",
                                                     min_text_length=1,
                                                     max_text_length=10, helper_text='0-100')

        self.update_filter_dialog()
        self.filter_dialog.open()

    def update_filter_dialog(self):
        if self.filter_dialog is not None:
            self.post_type_dropdown.text = self.post_type_filter
            self.sort_by_dropdown.text = self.sort_mode
            self.sort_order_dropdown.text = self.sort_order
            self.max_dist_field.text_field.text = self.max_dist_filter
            self.min_follows_field.text_field.text = self.min_follows_filter

    def reset_filters(self, d=None):
        self.post_type_filter = 'All'
        self.sort_mode = 'Distance'
        self.sort_order = 'Ascending'
        self.max_dist_filter = '10000'
        self.min_follows_filter = '0'
        self.custom_filters = False
        if self.filter_button is not None: self.filter_button.theme_icon_color = "Custom" if (
            self.custom_filters) else "Primary"
        if self.filter_dialog is not None:
            self.update_filter_dialog()
            self.make_gen_search()

    def apply_filters(self, d=None):
        if self.filter_dialog is not None:
            self.custom_filters = True
            self.filter_button.theme_icon_color = "Custom" if (self.custom_filters) else "Primary"
            self.post_type_filter = self.post_type_dropdown.text
            self.sort_mode = self.sort_by_dropdown.text
            self.sort_order = self.sort_order_dropdown.text
            self.max_dist_filter = self.max_dist_field.text_field.text
            self.min_follows_filter = self.min_follows_field.text_field.text
            if self.filter_dialog.open:
                self.close_filter_dialog()
            self.make_gen_search()

    def close_filter_dialog(self, d=None):
        self.filter_dialog.dismiss()

    def toggle_bookmarked_only(self, d=None):
        self.bookmarked_only = not self.bookmarked_only
        self.bookmarks_button.theme_icon_color = "Custom" if self.bookmarked_only else "Primary"
        if self.bookmarked_only:
            show_snackbar("Showing bookmarked posts")
        else:
            self.clear_results()
        Clock.schedule_once(self.make_gen_search, 0.1)

    def press_delete_advert(self, advert_id, d=None):
        delete_dialogue = DeleteAdvertDialogue(advert_id)
        delete_dialogue.on_confirm_actions.append(self.refresh_results)


filter_dialog_helper = """
BoxLayout:
    orientation: 'vertical'
    size_hint: (1,1)
    pos_hint: {'center_x':0.5,'center_y':0.5}  
"""


class FilterDialogContent(FloatLayout):
    pass


class DeleteAdvertDialogue():
    def __init__(self, advert_id):
        self.advert_id = advert_id
        self.on_confirm_actions = []
        self.dialog = MDDialog(title='Delete Advert?',
                               buttons=[MDFlatButton(text='Cancel', on_release=partial(self.cancel)),
                                        MDFlatButton(text='Confirm', on_release=partial(self.confirm))])
        self.dialog.open()

    def confirm(self, d=None):
        show_snackbar(delete_advert(self.advert_id))
        self.dialog.dismiss()
        for action in self.on_confirm_actions:
            action()
        del self.dialog
        del self

    def cancel(self, d=None):
        self.dialog.dismiss()
        del self.dialog
        del self
