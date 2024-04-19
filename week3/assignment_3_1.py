'''
Spot Parse
"info":"搭乘捷運淡水線至士林站下車，轉乘 紅 30（低地板公車） 往故宮博物院至本院正館門口下車。或轉乘公車 255、304、815（三重-故宮博物院）、小型公車 18 、小型公車 19 於本院正面廣場前下車。 搭乘捷運文湖線至大直站下車，轉乘 棕 13 往故宮博物院至本院正面廣場前下車。或搭乘捷運文湖線至劍南路站下車，轉乘 棕 20 往故宮博物院至本院正館門口下車。",
"stitle":"國立故宮博物院",
"xpostDate":"2016\/07\/06",
"longitude":"121.5496",
"REF_WP":"10",
"avBegin":"2008\/08\/12",
"langinfo":"10",
"SERIAL_NO":"2011051800000092",
"RowNumber":"4",
"CAT1":"景點",
"CAT2":"藝文館所",
"MEMO_TIME":"展覽區一（正館）：全年開放，上午八時三十分至下午六時三十分。\n夜間延長開放時段：每週五、週六18:30～21:00，國人憑身分證件可免費參觀。 \n(其他館開放時間請參閱國立故宮博物院官網：https:\/\/www.npm.gov.tw\/zh-TW\/Article.aspx?sNo=03000063)",
"POI":"Y",
"filelist":"https:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/image\/A0\/B0\/C0\/D14\/E810\/F21\/48d66fbd-1ba3-4efd-837a-3767db5f52e0.jpghttps:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/pic\/11000721.jpghttps:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/pic\/11000723.jpghttps:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/pic\/11000722.jpghttps:\/\/www.travel.taipei\/streams\/scenery_file_audio\/c18.mp3",
"idpt":"臺北旅遊網",
"latitude":"25.1013",
"xbody":"國立故宮博物院於1965年在外雙溪落成，中國宮殿式的建築，一至三樓為展覽陳列空間，四樓為休憩茶座「三希堂」，藏有全世界最多的中華藝術寶藏，收藏品主要承襲自宋、元、明、清四朝，幾乎涵蓋了整部五千年的中國歷史，數量達65萬多件，國立故宮博物院擁有「中華文化寶庫」的美名。國立故宮博物院除了展覽品豐富以外，提供中、英、法、德、日、西、韓等七國語言專業導覽，並定期舉辦各類文物研習課程、專題演講及巡迴展出活動，出版百種以上的刊物及專輯，實為世界的文化寶地，國立故宮博物院是來臺灣旅遊的必訪之地。 ",
"_id":4,
"avEnd":"2016\/07\/06"
'''
'''
MRT parse
"MRT":"文德",
"SERIAL_NO":"2011051800000646",
"address":"臺北市 內湖區內湖路2段175號"
'''

import urllib.request as request
import csv
import json

# URL of the source data
spot_url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
mrt_url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

# Open the URL and read the content
with request.urlopen(spot_url) as response:
    content = response.read().decode("utf-8")
    # Parse the JSON data
    spot_data = json.loads(content)

with request.urlopen(mrt_url) as response:
    station = response.read().decode("utf-8")
    # Parse the JSON data
    mrt_data = json.loads(station)

#the data format in the json
spot_data = spot_data["data"]["results"]
mrt_data = mrt_data["data"]

def get_district(address):
    if address.startswith("臺北市"):
        # Extract the substring between "臺北市" and "區"
        district = address[3:8]
        return district
    else:
        return None
    
def get_first_image(filelist):
    image = filelist.split("https://www.travel.taipei")

    # Find the first element containing ".JPG" or ".jpg" (case-insensitive)
    first_image_url = None
    for url in image:
        if url.lower().endswith(".jpg"):
            first_image_url = "https://www.travel.taipei" + url
            break
    return first_image_url
 
spot_output = []
mrt_output = {}
mapping = []

#map the district to spot via serial_no into a joint list
for i in range(len(spot_data)):
    for j in range(len(mrt_data)):
        if spot_data[i]["SERIAL_NO"] == mrt_data[j]["SERIAL_NO"]:
            mapping.append({**spot_data[i], **mrt_data[j]})
            #print(mapping)

#extract the spot data
for i in range(len(mapping)-1):
    filtered_data = {key: value for key, value in mapping[i].items() if key in ["stitle", "address", "longitude", "latitude", "filelist"]}
    spot_output.append(filtered_data)
    #print(spot_output)
    #extract the district from address
    spot_output[i]["address"] = get_district(spot_output[i]["address"])
    #extract the first image URL
    spot_output[i]["filelist"] = get_first_image(spot_output[i]["filelist"])
    #print(spot_output)
    # Reorder keys directly within spot_output
    desired_order = ["stitle", "address", "longitude", "latitude", "filelist"]
    spot_output[i] = {key: spot_output[i].get(key) for key in desired_order}
    #print(spot_output)

#group the spot data by MRT station
for i in range(len(mapping)):
    mrt = mapping[i]["MRT"]
    if mrt:
        if mrt not in mrt_output:
            mrt_output[mrt] = []
        mrt_output[mrt].append(mapping[i]["stitle"])

# Write the spot data to a CSV file
#SpotTitle,District,Longitude,Latitude,ImageURL
header = ["SpotTitle", "district", "longitude", "latitude", "first_image_url"]
with open("spot.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer_spot = csv.writer(csvfile)
    writer_spot.writerow(header)
    for row in spot_output:
        # Access value from dictionary using the key (row)
        writer_spot.writerow(row.values())

#write mrt data to a csv file
#StationName,AttractionTitle1,AttractionTitle2,AttractionTitle3,...
with open("mrt.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer_mrt = csv.writer(csvfile)
    for key, values in mrt_output.items():
        row = []
        row.append(key)
        row.extend(values)
        writer_mrt.writerow(row)
