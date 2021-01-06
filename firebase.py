import requests
import json
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
import urllib
from devices import DeviceBanner


name = None

class MyFireBase:
    wak = "AIzaSyCkBT7Dcr3k2wLxfaOrRL2_R3C3leTwwdI"   #web api key


    def signup_success(self,req,data):
        print(data)
        refresh_token = data["refreshToken"]
        localId = data["localId"]
        idToken = data["idToken"]
        with open("refresh_token.txt", "w") as f:
            f.write(refresh_token)

        MDApp.get_running_app().localId = localId
        MDApp.get_running_app().idToken = idToken

        print(MDApp.get_running_app().get_location())
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

        device_name = MDApp.get_running_app().device_name

        my_data = json.dumps({'name': str(name), 'phones': {str(device_name): {'latest_lat': 10, 'latest_lon': 10}}, 'currentPhone': str(device_name)})
        UrlRequest("https://track-buddy-9b27e-default-rtdb.firebaseio.com/" + localId + ".json?auth=" + idToken, req_body=my_data,req_headers=headers)

        my_data = json.loads(my_data)
        MDApp.get_running_app().root.ids["homescreen"].ids["homescreen_title"].text = my_data["name"]

        for phone in my_data["phones"]:
            banner = DeviceBanner(device_name=str(phone))
            MDApp.get_running_app().root.ids["homescreen"].ids["devices"].add_widget(banner)


        MDApp.get_running_app().change_screen("homescreen")

    def signup_error(self,req, data):
        print(data)


    def signup(self, root, username, email, password):
        global name
        name = username
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" +self.wak
        signup_data = urllib.parse.urlencode({'email':email,'password':password, 'returnSecureToken':True})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        UrlRequest(url=signup_url, on_success=self.signup_success,on_error=self.signup_error, req_body=signup_data,on_failure=self.signup_error,
                   req_headers=headers)
        print("here")


    def sign_in_existing_user(self, root, email, password):
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
        signin_payload = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_payload)
        sign_up_data = json.loads(signin_request.content.decode())
        print(sign_up_data)
        if signin_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            MDApp.get_running_app().localId = localId
            MDApp.get_running_app().idToken = idToken

            MDApp.get_running_app().on_start()
        elif signin_request.ok == False:
            error_data = json.loads(signin_request.content.decode())
            error_message = error_data["error"]['message']
            root.ids['error_msg_login'] = "EMAIL EXISTS - " + error_message.replace("_", " ")


    def exchange_refresh_token(self,refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type":"refresh_token","refresh_token":"%s"}' % refresh_token
        refresh_request = requests.post(refresh_url,refresh_payload)

        local_id = refresh_request.json()["user_id"]
        id_token = refresh_request.json()["id_token"]

        return id_token, local_id
