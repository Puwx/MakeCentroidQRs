import os
import time
import json
import urllib
import requests

import numpy as np

def makeCentQRCode(output_location,geojson_file):
    """
    Usage:
    Not extremely useful - FYI

    GeoJSON format changes, so the **coords** line might have to be altered (change indices) to work

    Give function an output folder (location where QC codes will be exported to) and a geojson file (formatted same a QGIS export - pretty sure)

    Will create 150x150 black and white QR codes 
    """
    baseGoogUrl = r"https://www.google.com/maps/place/"
    qrCode = r"https://api.qrserver.com/v1/create-qr-code/?data={}&size=150x150"

    geoms = json.loads(open(geojson_file,"r").read())

    cnt = 1
    for g in geoms["features"]:
        coords = g["geometry"]["coordinates"][0][0]
        centX = np.array(coords)[:,0].mean()
        centY = np.array(coords)[:,1].mean()

        googUrl = baseGoogUrl + "{},{}".format(centY,centX)
        urlComplete = urllib.parse.quote(googUrl)
        reqObj = requests.get(qrCode.format(urlComplete))
        
        with open(os.path.join(output_location,f"QC_CODE{cnt}.png"),"wb") as outImg:
            outImg.write(reqObj.content)
        cnt+=1
        time.sleep(0.5)
