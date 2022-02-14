#import matplotlib.pyplot as plt
#from matplotlib.colors import LogNorm
import ctypes as ct
import os

from sdk import WfsLib

try:
    from .helper import log
except:
    from helper import log

import matplotlib.pyplot as plt

WFS_RESOLUTIONS = {
    'WFS150-7AR':
        [    
            ('CAM_RES_1280', (1280,1024)),
            ('CAM_RES_1024', (1024,1024)),
            ('CAM_RES_768', (768,768)),
            ('CAM_RES_512', (512,512)),
            ('CAM_RES_320', (320,320))
        ],
    'WFS10':
        [
            ('CAM_RES_WFS10_640', (640,480)),
            ('CAM_RES_WFS10_480', (480,480)),
            ('CAM_RES_WFS10_360', (360,360)),
            ('CAM_RES_WFS10_260', (260,260)),
            ('CAM_RES_WFS10_180', (180,180)),
        ]
}

# Get dll
dll_dir = "C:\Program Files (x86)\Thorlabs\Wavefront Sensor"
dll_name = "WFS_64.dll"
dll_path = os.path.join(dll_dir, dll_name)
dll = ct.CDLL(dll_path)

# List devices
lib = WfsLib(dll)

# Get device handle
wfs = lib.open(list_index=0)

# List and select MLA
wfs.get_mla_info()
wfs.set_mla(mla_index=0)

# configuration
wfs.set_resolution(cam_resol_index=0) # 1280, 1024 for WFS150
wfs.set_reference_plane(internal=True)
wfs.set_pupil(center=[0, 0], diameter=[3,3])

# Capture image and peform wavefront calculation
# repeat at most 3 times
for i in range(3):
    wfs.take_spot_field_image_auto_expos()
    status = wfs.get_status()
    # check if parameters are right
    print(status)
    if (not status["PTH"]) and (not status["PTL"]) and (not status["HAL"]):
        break

try:
    wfs.take_spot_field_image_auto_expos()
    result = wfs.get_spot_field_image_copy()
    print(result)
    #
    plt.imshow(result)
    plt.colorbar()
    plt.show()
except Exception as e:
    log.critical(f"{e}")
finally:
    wfs.close()