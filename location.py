from plyer import gps
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform

lat = None
lon = None
gps_status = StringProperty('Click Start to get GPS location updates')


def get_location():
    try:
        gps.configure(on_location=on_location,
                      on_status=on_status)
        return lat, lon
    except NotImplementedError:
        import traceback
        traceback.print_exc()
        gps_status = 'GPS is not implemented for your platform'


@mainthread
def on_location(self, **kwargs):
    lat = kwargs["lat"]
    lon = kwargs["lon"]


@mainthread
def on_status(self, stype, status):
    self.gps_status = 'type={}\n{}'.format(stype, status)




