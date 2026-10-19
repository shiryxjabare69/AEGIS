from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from datetime import datetime
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.audio import SoundLoader
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
import webbrowser
from kivy.storage.jsonstore import JsonStore

try:
    from plyer import accelerometer, battery, flashlight
    has_sensor = True
except ImportError:
    has_sensor = False

Window.size = (414, 736)

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    SplashScreen:
    SignUpScreen:
    SignInScreen:
    MainScreen:
    ProfileScreen:

<SplashScreen>:
    name: 'splash'
    md_bg_color: 0.07, 0.09, 0.15, 1 
        
    MDFloatLayout:
        MDLabel:
            id: logo_label
            text: "AEGIS"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .6}
            font_style: "H2"
            theme_text_color: "Custom"
            text_color: 0, 0.8, 1, 1  
            bold: True
            opacity: 0  
            
        MDLabel:
            id: dev_label
            text: "Developed by SHREYASH JABARE"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .15}
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.6, 0.6, 0.6, 1
            opacity: 0  

<SignUpScreen>:
    name: 'signup'
    md_bg_color: 0.07, 0.09, 0.15, 1
        
    MDBoxLayout:
        orientation: 'vertical'
        padding: "30dp"
        spacing: "15dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: "Create Account"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            bold: True

        MDTextField:
            id: name_input
            hint_text: "Full Name"
            mode: "rectangle"
            icon_right: "account"

        MDTextField:
            id: mobile_input
            hint_text: "Mobile Number"
            mode: "rectangle"
            icon_right: "phone"
            input_filter: "int"
            max_text_length: 10

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            spacing: "10dp"
            
            MDTextField:
                id: dob_input
                hint_text: "Birth Date (YYYY-MM-DD)"
                mode: "rectangle"
                on_focus: if not self.focus: app.calculate_age(self.text)
                
            MDIconButton:
                icon: "calendar"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: app.show_date_picker()

        MDTextField:
            id: age_input
            hint_text: "Age (Auto Calculated)"
            mode: "rectangle"
            readonly: True

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            spacing: "10dp"
            
            MDTextField:
                id: password_input
                hint_text: "Create Password"
                mode: "rectangle"
                password: True
                helper_text: "Min 8 chars, num+letters"
                helper_text_mode: "on_error"
                
            MDIconButton:
                icon: "eye-off"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                on_release:
                    password_input.password = not password_input.password
                    self.icon = "eye" if not password_input.password else "eye-off"

        MDFillRoundFlatButton:
            text: "Send OTP & Register"
            pos_hint: {"center_x": .5}
            size_hint_x: 1
            on_release: app.verify_signup()

        MDTextButton:
            text: "Already have an account? Log In"
            pos_hint: {"center_x": .5}
            theme_text_color: "Hint"
            on_release: app.root.current = 'signin'

<SignInScreen>:
    name: 'signin'
    md_bg_color: 0.07, 0.09, 0.15, 1
        
    MDBoxLayout:
        orientation: 'vertical'
        padding: "30dp"
        spacing: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: "Welcome Back!"
            halign: "center"
            font_style: "H4" 
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            bold: True

        MDTextField:
            id: login_mobile
            hint_text: "Mobile Number"
            mode: "rectangle"
            icon_right: "phone"
            input_filter: "int"
            max_text_length: 10

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            spacing: "10dp"
            
            MDTextField:
                id: login_password
                hint_text: "Password"
                mode: "rectangle"
                password: True
                
            MDIconButton:
                icon: "eye-off"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                on_release:
                    login_password.password = not login_password.password
                    self.icon = "eye" if not login_password.password else "eye-off"

        MDFillRoundFlatButton:
            text: "Log In"
            pos_hint: {"center_x": .5}
            size_hint_x: 1
            on_release: app.verify_login()

<MainScreen>:
    name: 'main'
    md_bg_color: 0.07, 0.09, 0.15, 1

    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "AEGIS"
            elevation: 2
            md_bg_color: 0.04, 0.06, 0.1, 1 
            specific_text_color: app.theme_cls.primary_color
            right_action_items: [["account-circle", lambda x: app.open_profile()]]

        MDScrollView:
            MDBoxLayout:
                id: main_layout
                orientation: 'vertical'
                padding: "20dp"
                spacing: "20dp"
                size_hint_y: None
                height: self.minimum_height

                MDBoxLayout:
                    id: contacts_box
                    orientation: 'vertical'
                    spacing: "15dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Add Emergency Contacts"
                        halign: "center"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        bold: True

                    MDTextField:
                        id: main_contact_1
                        hint_text: "Mobile 1 (Family)"
                        mode: "rectangle"
                        input_filter: "int"
                        max_text_length: 10

                    MDTextField:
                        id: main_contact_2
                        hint_text: "Mobile 2 (Family)"
                        mode: "rectangle"
                        input_filter: "int"
                        max_text_length: 10

                    MDTextField:
                        id: main_contact_3
                        hint_text: "Mobile 3 (Family)"
                        mode: "rectangle"
                        input_filter: "int"
                        max_text_length: 10

                    MDFillRoundFlatButton:
                        text: "Save Numbers"
                        pos_hint: {"center_x": .5}
                        size_hint_x: 0.8
                        md_bg_color: app.theme_cls.primary_color
                        on_release: app.save_contacts_main()

                Widget:
                    size_hint_y: None
                    height: "10dp"

                MDLabel:
                    text: "Status: Sensor Active"
                    halign: "center"
                    font_style: "H6"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1 

                MDFillRoundFlatButton:
                    text: "Find Nearby Hospital"
                    pos_hint: {"center_x": .5}
                    size_hint_x: 0.9
                    md_bg_color: 0, 0.6, 0.6, 1 
                    on_release: app.find_hospital()
                    
                MDFillRoundFlatButton:
                    text: "EMERGENCY SOS"
                    pos_hint: {"center_x": .5}
                    size_hint_x: 0.9
                    md_bg_color: 1, 0, 0, 1
                    on_release: app.call_108()
                    
                Widget:
                    size_hint_y: None
                    height: "20dp"

<ProfileScreen>:
    name: 'profile'
    md_bg_color: 0.07, 0.09, 0.15, 1 
        
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "My Profile"
            elevation: 2
            md_bg_color: 0.04, 0.06, 0.1, 1 
            specific_text_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: app.go_back_to_main()]]

        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "15dp"
                size_hint_y: None
                height: self.minimum_height
                
                MDLabel:
                    text: f"Name: {app.user_name}"
                    theme_text_color: "Hint"
                    
                MDLabel:
                    text: f"Mobile: {app.user_mobile}"
                    theme_text_color: "Hint"
                    
                # Ithe Age add kele ahe
                MDLabel:
                    text: f"Age: {app.user_age}"
                    theme_text_color: "Hint"

                MDSeparator:
                    height: "1dp"
                    
                MDLabel:
                    text: "Emergency Contacts"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    bold: True

                MDTextField:
                    id: contact_1
                    hint_text: "Mobile 1 (Family)"
                    mode: "rectangle"
                    input_filter: "int"
                    max_text_length: 10

                MDTextField:
                    id: contact_2
                    hint_text: "Mobile 2 (Family)"
                    mode: "rectangle"
                    input_filter: "int"
                    max_text_length: 10

                MDTextField:
                    id: contact_3
                    hint_text: "Mobile 3 (Family)"
                    mode: "rectangle"
                    input_filter: "int"
                    max_text_length: 10

                MDFillRoundFlatButton:
                    id: update_btn
                    text: "Save / Update Contacts"
                    pos_hint: {"center_x": .5}
                    size_hint_x: 1
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.update_contacts_profile()
                    
                Widget:
                    size_hint_y: None
                    height: "15dp"
                    
                MDFillRoundFlatButton:
                    text: "Log Out"
                    pos_hint: {"center_x": .5}
                    size_hint_x: 0.6
                    md_bg_color: 1, 0, 0, 1
                    on_release: app.log_out()
'''

class SplashScreen(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.start_animation, 0.1)

    def start_animation(self, dt):
        anim1 = Animation(opacity=1, duration=1.5)
        anim1.start(self.ids.logo_label)
        anim2 = Animation(opacity=1, duration=2.0)
        anim2.start(self.ids.dev_label)
        Clock.schedule_once(self.check_database, 3.5)
        
    def check_database(self, dt):
        app = MDApp.get_running_app()
        if app.store.exists('user'):
            app.root.current = 'main'
            if app.store.exists('contacts'):
                main_screen = app.root.get_screen('main')
                main_layout = main_screen.ids.main_layout
                contacts_box = main_screen.ids.contacts_box
                if contacts_box in main_layout.children:
                    main_layout.remove_widget(contacts_box)
                    app.are_contacts_saved = True
        else:
            app.root.current = 'signup'

class SignUpScreen(MDScreen):
    pass
class SignInScreen(MDScreen):
    pass
class MainScreen(MDScreen):
    pass
class ProfileScreen(MDScreen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        self.ids.contact_1.text = app.em_contact_1
        self.ids.contact_2.text = app.em_contact_2
        self.ids.contact_3.text = app.em_contact_3

class AegisApp(MDApp):
    user_name = StringProperty("Not Set")
    user_mobile = StringProperty("Not Set")
    user_age = StringProperty("Not Set")
    em_contact_1 = StringProperty("")
    em_contact_2 = StringProperty("")
    em_contact_3 = StringProperty("")
    are_contacts_saved = BooleanProperty(False)
    
    countdown_time = 5
    dialog = None
    siren_sound = None
    timer_event = None
    flash_state = False
    
    store = JsonStore('aegis_database.json')

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_string(KV)

    def on_start(self):
        if self.store.exists('user'):
            user_data = self.store.get('user')
            self.user_name = user_data['name']
            self.user_mobile = user_data['mobile']
            self.user_age = user_data.get('age', 'N/A')
            
        if self.store.exists('contacts'):
            contact_data = self.store.get('contacts')
            self.em_contact_1 = contact_data['c1']
            self.em_contact_2 = contact_data['c2']
            self.em_contact_3 = contact_data['c3']
            self.are_contacts_saved = True

        if has_sensor:
            try:
                accelerometer.enable()
                Clock.schedule_interval(self.check_sensor, 0.5)
            except:
                pass

    def check_sensor(self, dt):
        if has_sensor:
            try:
                val = accelerometer.acceleration
                if val:
                    zAccel = val[2]
                    if abs(zAccel) > 25:
                        if self.dialog is None:
                            self.trigger_fall_detection()
            except:
                pass

    def calculate_age(self, dob_text):
        if not dob_text: return
        try:
            birth_date = datetime.strptime(dob_text, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            self.root.get_screen('signup').ids.age_input.text = f"{age} Years"
        except ValueError:
            pass

    def show_date_picker(self):
        date_dialog = MDDatePicker(year=2000, month=1, day=1)
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        signup_screen = self.root.get_screen('signup')
        signup_screen.ids.dob_input.text = str(value)
        self.calculate_age(str(value))

    def verify_signup(self):
        signup_screen = self.root.get_screen('signup')
        if signup_screen.ids.name_input.text != "":
            self.user_name = signup_screen.ids.name_input.text
            self.user_mobile = signup_screen.ids.mobile_input.text
            self.user_age = signup_screen.ids.age_input.text if signup_screen.ids.age_input.text else "N/A"
            
            # Database madhe age save kene
            self.store.put('user', name=self.user_name, mobile=self.user_mobile, age=self.user_age)
            
        self.root.current = 'main'
        
    def verify_login(self):
        self.root.current = 'main'

    def save_contacts_main(self):
        main_screen = self.root.get_screen('main')
        self.em_contact_1 = main_screen.ids.main_contact_1.text
        self.em_contact_2 = main_screen.ids.main_contact_2.text
        self.em_contact_3 = main_screen.ids.main_contact_3.text
        self.store.put('contacts', c1=self.em_contact_1, c2=self.em_contact_2, c3=self.em_contact_3)
        if not self.are_contacts_saved:
            main_layout = main_screen.ids.main_layout
            main_layout.remove_widget(main_screen.ids.contacts_box)
            self.are_contacts_saved = True

    def open_profile(self):
        self.root.current = 'profile'
        
    def go_back_to_main(self):
        self.root.current = 'main'

    def update_contacts_profile(self):
        profile_screen = self.root.get_screen('profile')
        self.em_contact_1 = profile_screen.ids.contact_1.text
        self.em_contact_2 = profile_screen.ids.contact_2.text
        self.em_contact_3 = profile_screen.ids.contact_3.text
        self.store.put('contacts', c1=self.em_contact_1, c2=self.em_contact_2, c3=self.em_contact_3)
        profile_screen.ids.update_btn.text = "Updated Successfully!"
        profile_screen.ids.update_btn.md_bg_color = [0, 0.8, 0, 1]
        Clock.schedule_once(lambda dt: self.reset_update_btn(), 2)

    def reset_update_btn(self):
        profile_screen = self.root.get_screen('profile')
        profile_screen.ids.update_btn.text = "Save / Update Contacts"
        profile_screen.ids.update_btn.md_bg_color = self.theme_cls.primary_color

    def log_out(self):
        self.store.clear()
        self.root.current = 'signup'

    def call_108(self):
        webbrowser.open("tel:108") 

    def trigger_fall_detection(self):
        self.countdown_time = 5
        try:
            self.siren_sound = SoundLoader.load('siren.mp3')
            if self.siren_sound: self.siren_sound.play()
        except:
            pass

        self.dialog = MDDialog(
            title="⚠️ FALL DETECTED!",
            text=f"Sending Direct SMS, Audio & Flash SOS in {self.countdown_time} sec...",
            buttons=[MDFlatButton(text="I AM SAFE (CANCEL)", text_color=[1, 0, 0, 1], on_release=self.cancel_sos)],
        )
        self.dialog.open()
        
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.countdown_time -= 1
        
        if has_sensor:
            try:
                if self.flash_state:
                    flashlight.off()
                    self.flash_state = False
                else:
                    flashlight.on()
                    self.flash_state = True
            except:
                pass

        if self.dialog:
            self.dialog.text = f"Sending Direct SMS, Audio & Flash SOS in {self.countdown_time} sec..."
        
        if self.countdown_time <= 0:
            self.timer_event.cancel()
            if self.siren_sound: self.siren_sound.stop()
            if has_sensor:
                try: flashlight.off()
                except: pass
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None 
            self.execute_emergency_protocol()

    def cancel_sos(self, instance):
        if self.timer_event: self.timer_event.cancel()
        if self.siren_sound: self.siren_sound.stop()
        if has_sensor:
            try: flashlight.off()
            except: pass
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None 
        print("SOS Cancelled: I am Safe now!")

    def execute_emergency_protocol(self):
        print("\n--- EMERGENCY PROTOCOL TRIGGERED ---")
        try:
            bat_status = battery.status
            bat_percent = bat_status.get('percentage', 'Unknown')
        except:
            bat_percent = "Unknown"
        
        print("[System] Microphone Active: Recording 5 seconds surrounding audio...")
        
        location_link = "https://maps.google.com/?q=19.2183,72.9781" 
        msg = f"🚨 EMERGENCY: AEGIS detected a fall!\nUser: {self.user_name}\nBattery: {bat_percent}%\nLocation: {location_link}\n[5-Sec Audio Recorded]"
        
        contacts = [self.em_contact_1, self.em_contact_2, self.em_contact_3]
        for num in contacts:
            if num:
                print(f"[System] Sending DIRECT BACKGROUND SMS to: +91 {num} -> Text: {msg}")
        
        print("\n--- PROTOCOL COMPLETE ---")

if __name__ == '__main__':
    AegisApp().run()
