from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import pyttsx3
engine = pyttsx3.init()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def decrease():
    current = volume.GetMasterVolumeLevel()
    print("Decreasing volume")
    engine.say("Decreasing volume")
    engine.runAndWait()
    return volume.SetMasterVolumeLevel(current - 6.0, None)


def increase():
    current = volume.GetMasterVolumeLevel()
    print("Increasing volume")
    engine.say("Increasing volume")
    engine.runAndWait()
    return volume.SetMasterVolumeLevel(current + 6.0, None)


def mute(self):
    return volume.SetMute(1, None)


def decrease_():
    current = sbc.get_brightness(display=0)
    return sbc.set_brightness()


def increase_():
    current = sbc.get_brightness(display=0)
    return sbc.set_brightness(current + 6.0)
