from kivymd.uix.screen import Screen
from Frontend.Screens.OuterScreens.LoginForm import LoginScreen
from Frontend.Screens.OuterScreens.RegisterForm import RegisterDetailsScreen
from Frontend.Screens.InnerScreens.HomeForm import HomeScreen
from Frontend.Screens.InnerScreens.PostAdvertForm import PostAdvertScreen
from Frontend.Screens.InnerScreens.ProfileForm import ProfileScreen
from Frontend.Screens.InnerScreens.SettingsForm import SettingsScreen
from Frontend.Screens.InnerScreens.EditDetailsForm import EditDetailsScreen
from Frontend.Screens.InnerScreens.AdvertView import AdvertViewScreen
from Frontend.Screens.InnerScreens.AdminForm import AdminScreen
from Frontend.Screens.InnerScreens.SupportChat import SupportChatScreen
from Frontend.CustomTools.AdvertWidgets import FilterDialogContent

main_helper = """
Screen:
    MDNavigationLayout:
        ScreenManager: #Navigation layout ONLY TAKES nav drawer and screenmanager
            id: outer_screen_manager 
            OuterHomeScreen:
            InnerScreen:
                id: inner_screen
            LoginScreen:
            RegisterDetailsScreen:
        MDNavigationDrawer:
            id: nav_drawer
            size_hint_x: None
            width: '180'
            BoxLayout:
                orientation: 'vertical'
                spacing: '3dp'
                padding: '3dp'
                Image:
                    id: profile_picture
                    source: ''
                    size_hint_x: 1
                    size_hint_y: None
                    width: '150dp'
                    height: '150dp'
                MDLabel:
                    id: username_label
                    text: 'Username'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    id: email_label
                    text: 'sampleemail@mail.com'
                    font_style: 'Caption'
                    size_hint_y: None
                    height: self.texture_size[1]
                #:import ScrollEffect  kivy.effects.scroll.ScrollEffect
                ScrollView:
                    effect_y: ScrollEffect() #To prevent default bouncy dampening effect
                    do_scroll_x: False
                    size_hint_x: 1.2
                    pos_hint: {'center_x':0.5}
                    MDList:
                        size_hint_x: 2
                        OneLineIconListItem:
                            text: 'Profile'
                            on_press: app.go_to_profile_screen('current_user')
                            IconLeftWidget:
                                icon: 'face-man-outline'
                        OneLineIconListItem:
                            text: 'Upload'
                            on_press: app.change_inner_screen('post_advert')
                            IconLeftWidget:
                                icon: 'plus'
                        OneLineIconListItem:
                            on_press: app.change_inner_screen('settings')
                            text: 'Settings'
                            IconLeftWidget:
                                icon: 'cog'
                        OneLineIconListItem:
                            on_press: app.change_outer_screen('outer_home')
                            text: 'Logout'
                            IconLeftWidget:
                                icon: 'logout'
                        OneLineIconListItem:
                            id: support_button
                            on_press: app.change_inner_screen('support_chat')
                            text: 'Chat'
                            IconLeftWidget:
                                icon: 'chat-question'
                        OneLineIconListItem:
                            id: admin_button
                            on_press: app.change_inner_screen('admin')
                            text: 'Admin'
                            IconLeftWidget:
                                icon: 'account-alert'

#Outer Screens
<OuterHomeScreen>:
    name: 'outer_home'
    canvas.before:
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)

        MDLabel:
            text: 'Welcome to FoodShare'
            font_style: 'H3'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            theme_text_color: 'Secondary'

        Image:
            source: 'Images/logo.png'
            size_hint_y: None
            height: dp(200)  # Adjust the height as needed
            allow_stretch: True
            keep_ratio: True

        Widget:
            size_hint_y: None
            height: dp(50)  # Adjust the height as needed

        MDRaisedButton:
            text: 'Sign In'
            size_hint: (None, None)
            size: dp(200), dp(48)  # Adjust the size as needed
            pos_hint: {'center_x' : 0.5}
            elevation_normal: 5
            md_bg_color: app.theme_cls.primary_color
            on_press: app.change_outer_screen('login')

<InnerScreen>:
    name: 'inner_screen'
    BoxLayout:
        orientation: 'vertical'
        ScreenManager:
            id: inner_screen_manager
            ProfileScreen:
            HomeScreen:
            EditDetailsScreen:
            SettingsScreen:
            PostAdvertScreen:
            AdvertViewScreen:
            AdminScreen:
            SupportChatScreen:
        MDTopAppBar:
            id: toolbar
            title: 'Advert Feed'
            left_action_items: [["menu",lambda x: app.navigation_draw('toggle')]] #lambda stuff is for clicking
            right_action_items: [["home",lambda x: app.change_inner_screen('home')]]
            elevation: 2

<LoginScreen>:
    name: 'login'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
    MDLabel:
        text: 'Sign In'
        halign: 'center'
        pos_hint: {'center_x' : 0.5, 'center_y': 0.95}

<RegisterDetailsScreen>:
    name: 'register_details'
    ScrollView:
        size_hint: (1,1)
        #pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        BoxLayout:
            id: main_space
            orientation: 'vertical'
            size_hint: (1,None)
            #pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            height: "550dp"
            MDLabel:
                text: 'Sign Up'
                halign: 'center'
                #pos_hint: {'center_x' : 0.5, 'center_y': 0.95}


#Inner Screens
<HomeScreen>:
    name: 'home'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
        
<ProfileScreen>:
    name: 'profile'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
        
<EditDetailsScreen>:
    name: 'edit_details'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
        
<SettingsScreen>:
    name: 'settings'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
        
<PostAdvertScreen>:
    name: 'post_advert'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
    MDLabel:
        text: 'Post Advert'
        halign: 'center'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        
<AdvertViewScreen>:
    name: 'advert_view'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
        
<SupportChatScreen>:
    name: 'support_chat'
    FloatLayout:
        id: main_space
        size_hint: (1,1)       
        
        
<FilterDialogContent>
    #orientation: "vertical"
    #spacing: "6dp"
    size_hint_y: None
    height: "305dp"
    
<TCDialogContent>:
    size_hint_y: None
    height: "300dp"
    ScrollView:
        size_hint: (0.9, 0.9)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        FloatLayout:
            id: box_layout
            orientation: 'vertical'
            size_hint: (1,1.75)
    
<AdminScreen>:
    name: 'admin'
    FloatLayout:
        id: main_space
        size_hint: (1,1)
"""


class OuterHomeScreen(Screen):
    pass


class InnerScreen(Screen):
    pass
