from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRoundFlatButton
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest


class DeviceBanner(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super().__init__()

        fl = FloatLayout()
        label = MDLabel(text=kwargs["device_name"],size_hint=(0.5,0.5),pos_hint={"x":0, "y":0})
        button = MDRoundFlatButton(text="Track", size_hint=(0.5,0.5), pos_hint={"x":0.5,"y":0},on_release=self.mapview)

        fl.add_widget(label)
        fl.add_widget(button)

        self.add_widget(fl)


    def mapview(self,button):
        local_id = MDApp.get_running_app().localId
        id_token = MDApp.get_running_app().id_token

        UrlRequest("https://track-buddy-9b27e-default-rtdb.firebaseio.com/" + local_id + ".json?auth=" + id_token,
                   on_success=self.got_json)


    def got_json(self,req,data):

        for _,value in data.items():
            data = value

        lat = data["phones"]["AshutoshSudo"]["latest_lat"]
        lon = data["phones"]["AshutoshSudo"]["latest_lon"]

        MDApp.get_running_app().root.ids["map"].ids["mapview"].lat = lat
        MDApp.get_running_app().root.ids["map"].ids["mapview"].lat = lon

        MDApp.get_running_app().change_screen("mapscreen")

