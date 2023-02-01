from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

current = volume.GetMasterVolumeLevel()


def decrease():
    return volume.SetMasterVolumeLevel(current - 6.0, None)


def increase():
    return volume.SetMasterVolumeLevel(current + 6.0, None)