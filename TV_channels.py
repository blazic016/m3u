
import requests
from bs4 import BeautifulSoup
import re
import json

URL = "http://radiobox.info/srbija-tv-kanali/#/?playlistId=0&videoId=6"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

def Parsing_Data(source_data):
    #print(source)
    data=source_data.get("data-video-source")
    data_tmp = data.replace("[", "")
    data_tmp = data_tmp.replace("]", "")
    data_tmp = data_tmp.replace("'", "")
    data_tmp = data_tmp.replace("{", "")
    data_tmp = data_tmp.replace("}", "")
    data_tmp = data_tmp.replace("source:", "")
    data_tmp = data_tmp.replace("label:", "")
    data_tmp = data_tmp.replace("is360:", "")
    splitted = data_tmp.split(',')
    num_splitted = len(splitted)
    num_el = int(num_splitted/3)
    label_arr=[]
    img_arr=[]
    ts_arr=[]
    for i in range(num_el):
        ts = splitted[i*3]
        label = splitted[i*3+1]
        img = source_data.get("data-poster-source")
        ts = ts.replace(" ", "")
        label = label.replace(" ", "")
        img = img.replace(" ", "")
        # print("SOURCE: ", ts)
        # print("LABEL:", label)
        # print("IMG: ", img)
        label_arr.append(label)
        img_arr.append(img)
        ts_arr.append(ts)
    return ts_arr, label_arr, img_arr


num_channels=0
all_channel_arr = []
m3u_str="#EXTM3U\n"

for source in soup.find("ul", {"id": "fwduvpPlaylist0"}):
    num_channels=num_channels+1
    all_channel_arr.append(source)
    #print("--- ", num_channels, " --- ")
    #Parsing_Data(source)
    ts, label, img =  Parsing_Data(source)
    # print("SOURCE: ", ts)
    # print("LABEL:", label)
    # print("IMG: ", img)
    # print("lab=",len(label), " img=",len(img), " ts=", len(ts))
    for i in range(len(label)):
        # print(label[i])
        m3u_str += "#EXTINF:-1 tvg-id=\"xxx\" tvg-name=\"" + label[i] + "\" "
        m3u_str += "tvg-logo=\"" + img[i] + "\" "
        m3u_str += "group-title=\"Education\"," + label[i] 
        m3u_str += "\n"
        m3u_str += ts[i]
        m3u_str += "\n"

# for print_one_line in all_channel_arr:
#     print (print_one_line)



print(m3u_str)