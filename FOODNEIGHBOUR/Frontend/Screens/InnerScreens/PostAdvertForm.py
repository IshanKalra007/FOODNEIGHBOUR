from kivy.lang import Builder
from Backend.Class.CurrentUser import CurrentUser
from Frontend.CustomTools.CustomWidgets import ValidationField, show_snackbar
from Backend.Functions.AdvertFunc import add_advert
from Frontend.CustomTools.CustomWidgets import CustomScreen, user_data_field_helper, LocationPicker


buttons_helper = """
FloatLayout:
    MDRectangleFlatButton:
        text: 'Submit'
        pos_hint: {'center_x' : 0.5, 'center_y': 0.075}
        on_press: app.custom_screens['PostAdvert'].submit_donation_request()
    Button:
        id: type_button
        text: 'Select Advert Type'
        size_hint: None, None
        size: 200, 40
        pos_hint: {'center_x' : 0.5, 'center_y': 0.3}
        on_release: dropdown.open(self)
    DropDown:
        id: dropdown
        on_select: app.custom_screens['PostAdvert'].set_advert_type(args[1], type_button)
        Button:
            text: 'DONATION'
            size_hint_y: None
            height: '30dp'
            on_release: dropdown.select('DONATION')
        Button:
            text: 'REQUEST'
            size_hint_y: None
            height: '30dp'
            on_release: dropdown.select('REQUEST')
"""


class PostAdvertScreen(CustomScreen):
    def set_advert_type(self, advert_type, button):
        self.advert_type = advert_type
        button.text = advert_type

    # Inherited Methods
    def __init__(self, **kwargs):
        super(PostAdvertScreen, self).__init__(**kwargs)
        self.location_picker = None
        self.app.custom_screens['PostAdvert'] = self
        self.rebuild_on_load = True  # Rebuilds the screen every time it's switched to and clears when switched from
        self.top_seq_y = 0.9
        self.has_back_button = False
        self.advert_type = None

    def on_pre_enter(self):
        super().on_pre_enter()

    def on_pre_leave(self):
        super().on_pre_leave()

    def on_leave(self):
        super().on_leave()

    def build_screen(self):
        super().build_screen()

        # Input Fields
        self.validation_fields["TitleField"] = ValidationField(text_field_widget=self.sequential_add_widget(
            Builder.load_string(user_data_field_helper)),
            label="Title",
            min_text_length=1,
            max_text_length=100)

        self.validation_fields["DesignatedTimesField"] = ValidationField(text_field_widget=self.sequential_add_widget(
            Builder.load_string(user_data_field_helper)), label="Time", min_text_length=1,
            validation_check="UsersFunc.validate_datetime_format")

        self.location_picker = LocationPicker(CurrentUser().current_user.location)
        self.sequential_add_widget(self.location_picker.location_field.text_field)

        self.validation_fields["DescriptionField"] = ValidationField(text_field_widget=self.sequential_add_widget(
            Builder.load_string(user_data_field_helper)),
            label="Description",
            min_text_length=1,
            max_text_length=500)

        buttons = Builder.load_string(buttons_helper)
        self.dropdown = buttons.children[0]

        self.dropdown.dismiss()
        # Button
        self.main_space.add_widget(buttons)

    def clear_screen(self):
        super().clear_screen()
        del self.location_picker

    def submit_donation_request(self):
        if self.is_built:
            title = self.validation_fields['TitleField'].text
            time = self.validation_fields['DesignatedTimesField'].text
            postcode = "ST1 4AQ"
            description = self.validation_fields['DescriptionField'].text
            current_user = CurrentUser().current_user
            user_id = current_user.user_id

            valid_fields = self.validate_all_fields()

            self.location_picker.verify_location_text()
            location_coords = self.location_picker.cur_coords
            if self.advert_type is None:
                self.location_picker.location_field.error("Must specify type of advert")
            elif not self.location_picker.has_valid_coords:
                self.location_picker.location_field.error("Invalid address")
            elif valid_fields:  # if validate_all_fields function returns true (all fields are true)
                add_advert(title, description, postcode, time, self.advert_type, user_id, location_coords)  # add advert
                self.app.change_inner_screen("home")  # take user to home screen
                show_snackbar("Created Advert Successfully")

    def on_point_three_update(self, run_time):
        super().on_point_three_update(run_time)
        if self.is_built and self.location_picker is not None:
            self.location_picker.on_point_three_update(run_time)
