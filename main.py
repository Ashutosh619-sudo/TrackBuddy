from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from location import get_location
from firebase import MyFireBase
import json
import requests
import plyer
import platform
from devices import DeviceBanner
from kivy.network.urlrequest import UrlRequest



class LoginScreen(Screen):
    pass

class MapScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass

class HomeScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.id_token = None
        self.localId = None
        self.result = None
        self.get_location = get_location
        self.device_name = platform.node()
        self.my_firebase = MyFireBase()
        self.theme_cls.primary_palette = "Purple"

    def got_json(self, req, result):
        data = result
        print(result)

        for k,value in data.items():
            data = value

        self.root.ids["homescreen"].ids["homescreen_title"].text = data["name"]

        for phone in data["phones"]:
            banner = DeviceBanner(device_name=str(phone))
            self.root.ids["homescreen"].ids["devices"].add_widget(banner)

        self.change_screen("homescreen")

    def on_start(self):
        try:
            with open("refresh_token.txt", 'r') as f:
                refresh_token = f.read()

            self.id_token, self.localId = self.my_firebase.exchange_refresh_token(refresh_token)
            UrlRequest("https://track-buddy-9b27e-default-rtdb.firebaseio.com/"+self.localId+".json?auth="+ self.id_token, on_success=self.got_json)

        except Exception as e:
            print(e)

    def change_screen(self, screen_name):
        screen_manager = self.root
        screen_manager.current = screen_name



if  __name__ == "__main__":
    MainApp().run()

