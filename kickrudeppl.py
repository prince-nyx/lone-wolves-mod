import numpy as np
import cv2
import pyautogui as gui
import time
import asyncio
import discord
import os
import pytesseract
import re
import kickrudeppl_getusername
import csv
import removedubes

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\nyx\Downloads\Tesseract-OCR\tesseract.exe'

banned_weapons = {
    "mortar": [{
        "template": "",
        "shapes": "",
        "location": (0,0)
        }],
    "smg": [{
        "template": "",
        "shapes": "",
        "location": (0,0)
    }]
}

resize_val = 0.7
threshold = 0.9


def loadTemplateForBannedWeapons():
    template_path = os.getcwd() + "/templates"
    for files in os.listdir(template_path):
        template_temp = cv2.imread(f'{template_path}/{files}', 0)
        template_temp = cv2.cvtColor(np.array(template_temp, dtype=np.uint8), cv2.COLOR_GRAY2RGB)
        template_temp = cv2.cvtColor(np.array(template_temp, dtype=np.uint8), cv2.COLOR_RGB2GRAY)

        if re.search("mortar*", files):
            
            banned_weapons["mortar"].append(
            {
                "template": template_temp, 
                "shapes": template_temp.shape, 
                "location": template_temp.shape
            })
        else: 
            banned_weapons["smg"].append(
            {
                "template": template_temp, 
                "shapes": template_temp.shape, 
                "location": template_temp.shape
            })


hook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1283907164246769695/6hK0nGoqeQFwmWnE8-BSdTCFN9UbjZcqKw-W5VO573TFPhknUdU7RGHBuYDUZ2u1kF31")

loadTemplateForBannedWeapons()
method = cv2.TM_CCOEFF_NORMED #cv2.TM_CCORR_NORMED

#def getText(img, y, h):
#    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
#    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
#    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#
#    im2 = img.copy()
#
#    cnt_list = []
#    for cnt in contours:
#        x, y, w, h = cv2.boundingRect(cnt)
#        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
#        cv2.circle(im2, (x, y), 8, (255, 255, 0), 8)
#
#        cropped = im2[y:y + h, x:x + w]
#        text = pytesseract.image_to_string(cropped)
#        cnt_list.append([x,y,text])
#    return cnt_list


async def performTemplateMatch(img, img2):
    for weapon_type in banned_weapons:
        for idx, weapon_template_list in enumerate(banned_weapons[weapon_type]):
            if idx != 0:
                result = cv2.matchTemplate(img, banned_weapons[weapon_type][idx]["template"], method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val <= threshold:
                    color = bcolors.OKGREEN
                else: 
                    color = bcolors.FAIL
                print(f"checking for [{weapon_type}]:\t{color} {max_val} {bcolors.ENDC}")
                    
                if max_val >= threshold:
                    bottom_right = (max_loc[0] + banned_weapons[weapon_type][idx]["location"][1], max_loc[1] + banned_weapons[weapon_type][idx]["location"][0])
                    
                    filename = f'bad_person_{weapon_type}_{time.time()}.png'
                    filename2 = f"names/nametest_{time.time()}.png"
                    
                    img_cropped = img2[max_loc[1]:bottom_right[1], 1:max_loc[0]]

                    cv2.imwrite(filename2, img_cropped)
                    cv2.rectangle(img, max_loc, bottom_right, 255, 1)
                    cv2.imwrite(filename, img)
                    
                    try:
                        data = [
                            {'time': time.time(), 'weapon': weapon_type, 'name': str.upper(kickrudeppl_getusername.main(filename2)), 'path': filename2}
                        ]
                        with open('cock.csv', 'a', newline='') as csvfile:
                            fieldnames = ['time', 'weapon', 'name', 'path']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerows(data)
                    except:
                        continue
                    os.remove(filename)
                    cv2.destroyAllWindows()

cacheTimer = 0

while True:
    img = gui.screenshot(region=[1950,0,560,600])
    img3 = img.copy()
    img3 = np.array(img3, dtype=np.uint8)
    img = cv2.cvtColor(np.array(img, dtype=np.uint8), cv2.COLOR_RGB2GRAY)

    img_cropped = img3[80:200, 100:300]

    if time.time() >= cacheTimer + 30:
        cacheTimer = removedubes.main()
    
    print(f"time: {time.time()}")
    print(f"cache: {(cacheTimer +30) - time.time()}")

    img2 = img.copy()

    asyncio.run(performTemplateMatch(img2, img3)) 
    time.sleep(0.6)