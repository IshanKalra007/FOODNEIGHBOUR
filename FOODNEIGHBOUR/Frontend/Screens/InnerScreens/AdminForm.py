from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from sqlalchemy.orm import sessionmaker

from Backend.Class.CustomerSupport import CustomerSupport
from Frontend.CustomTools.CustomWidgets import CustomScreen, user_data_field_helper, ValidationField
from Frontend.CustomTools.UserWidgets import AdminSupportPopup
from Backend.Class.User import User
import Backend.Admin.Manage_Users as Manage_Users

from Main import engine

Session = sessionmaker(bind=engine)
session = Session()


class AdminScreen(CustomScreen):
    # Inherited Methods
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        self.app.custom_screens['Admin'] = self
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
        super().build_screen()

        # Query database for Row data
        users = session.query(
            User.user_id,
            User.user_name,
            User.user_email,
            User.user_mobile,
            User.user_postcode,
            User.user_type,
            User.user_flag_counter
        ).all()

        # Create tuple of user information for each user
        user_data = [(user.user_id,
                      user.user_name,
                      user.user_email,
                      user.user_mobile,
                      user.user_postcode,
                      user.user_type,
                      user.user_flag_counter)
                     for user in users]

        # Retrieve customer support requests
        support_requests = session.query(
            CustomerSupport.Support_Id,
            CustomerSupport.Email,
            CustomerSupport.Contact_Us,
            CustomerSupport.Issue_Description
        ).order_by(CustomerSupport.Email,
                   CustomerSupport.Support_Id).all()  # All fields are arranged by email address and ID

        # Create tuple of support request information for each request
        support_data = [(request.Support_Id,
                         request.Email,
                         request.Contact_Us,
                         request.Issue_Description)
                        for request in support_requests]

        # Input Fields
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_y=True)

        box_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=20, spacing=10)
        box_layout.bind(minimum_height=box_layout.setter('height'))

        spacer = MDLabel(text=' ', size_hint_y=None, height=950)

        # Remove User

        remove_user_label = MDLabel(text="Remove User", font_style="H6", size_hint_y=None, height=30, halign='center')

        self.validation_fields['RemoveUserField'] = ValidationField(
            text_field_widget=Builder.load_string(user_data_field_helper),
            label="Email Address")

        remove_user_button = MDRaisedButton(text="Update", size_hint_y=None, height=50, pos_hint={'center_x': 0.5})
        remove_user_button.bind(on_release=self.delete_user)

        # Change User Role

        change_role_label = MDLabel(text="Change User Role to Admin", font_style="H6", size_hint_y=None, height=30,
                                    halign='center')

        self.validation_fields['ChangeUserRoleField'] = ValidationField(
            text_field_widget=Builder.load_string(user_data_field_helper),
            label="Email Address")

        change_role_button = MDRaisedButton(text="Update", size_hint_y=None, height=50, pos_hint={'center_x': 0.5})
        change_role_button.bind(on_release=self.change_role)

        # User Table
        user_table_label = MDLabel(text="User Table", font_style="H6", size_hint_y=None, height=40, halign='center')

        user_table = MDDataTable(
            size_hint=(1, 0),
            height=dp(375),
            rows_num=len(user_data),
            column_data=[
                ('User ID', dp(20)),
                ('Username', dp(20)),
                ('Email Address', dp(40)),
                ('Phone Number', dp(30)),
                ('Postcode', dp(30)),
                ('User Type', dp(30)),
                ('Flags', dp(20))
            ],
            row_data=user_data)

        user_table.bind(on_row_press=self.on_row_press)

        # Support Requests Table
        support_table_label = MDLabel(text="Support Requests Table", font_style="H6", size_hint_y=None, height=60,
                                      halign='center')

        support_table = MDDataTable(
            size_hint=(1, 0),
            height=dp(375),
            rows_num=len(support_data),
            column_data=[
                ('Support ID', dp(20)),
                ('Email address', dp(40)),
                ('Mobile Phone', dp(40)),
                ('Description', dp(80))
            ],
            row_data=support_data
        )

        # Reply user
        reply_user_button = MDRaisedButton(text="Reply", size_hint_y=None, height=50, pos_hint={'center_x': 0.5})
        reply_user_button.bind(on_release=self.reply_button_press)

        # Add all widgets to box_layout
        box_layout.add_widget(spacer)
        box_layout.add_widget(remove_user_label)
        box_layout.add_widget(self.validation_fields['RemoveUserField'].text_field)
        box_layout.add_widget(remove_user_button)
        box_layout.add_widget(change_role_label)
        box_layout.add_widget(self.validation_fields['ChangeUserRoleField'].text_field)
        box_layout.add_widget(change_role_button)
        box_layout.add_widget(user_table_label)
        box_layout.add_widget(user_table)
        box_layout.add_widget(support_table_label)
        box_layout.add_widget(support_table)
        box_layout.add_widget(reply_user_button)

        # Adding the BoxLayout to the ScrollView
        scroll_view.add_widget(box_layout)

        # Adding the ScrollView to the main layout
        self.main_space.add_widget(scroll_view)

    def clear_screen(self):
        super().clear_screen()

    def on_row_press(self, instance_table, instance_row):
        row_num = int(instance_row.index / len(instance_table.column_data))
        self.app.go_to_profile_screen(str(instance_table.row_data[row_num][0]))

    def delete_user(self, obj):
        email = self.validation_fields['RemoveUserField'].text
        Manage_Users.remove_user(email)
        self.refresh_screen()

    def change_role(self, obj):
        email = self.validation_fields['ChangeUserRoleField'].text
        Manage_Users.change_user_role(email)
        self.refresh_screen()

    def reply_button_press(self, instance):
        response_popup = AdminSupportPopup(submit_callback=self.handle_response_submit)
        response_popup.open()

    def handle_response_submit(self, contact_us, email, support_input):
        print("Submitted comment:", support_input)
        create_support_form(contact_us, email, support_input)


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
