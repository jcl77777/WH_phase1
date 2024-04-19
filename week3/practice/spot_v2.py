import urllib.request as request
import csv
import json
import re


# URL of the source data (replace with actual URLs if they've changed)
spot_url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
mrt_url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

# Function to extract district information from address
def get_district(address):
    if address.startswith("臺北市") and address.endswith("區"):
        # Extract the substring between "臺北市" and "區"
        district = address[3:8]
        return district
    else:
        return None

# Open URL, read content, and parse JSON data (attractions)
with request.urlopen(spot_url) as response:
    content = response.read().decode("utf-8")
    attractions_data = json.loads(content)

# Open URL, read content, and parse JSON data (MRT stations)
with request.urlopen(mrt_url) as response:
    content = response.read().decode("utf-8")
    mrt_data = json.loads(content)

# Open CSV file for writing
with open("spot.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row (modify based on actual data keys)
    writer.writerow(["id", "SpotTitle", "District", "longitude", "latitude", "first_image_url"])  

    # Loop through each spot in the attractions data
    for spot in attractions_data["data"]["results"]:
        id = spot["_id"]
        SpotTitle = spot["stitle"]
        longitude = spot["longitude"]
        latitude = spot["latitude"]

        image = spot["filelist"].split("https://www.travel.taipei")
        # Find the first element containing ".JPG" or ".jpg" (case-insensitive)
        first_image_url = None
        for url in image:
            if url.lower().endswith(".jpg"):
                first_image_url = "https://www.travel.taipei" + url
                break
        
    for spot in mrt_data["data"]:
    # Extract address information
        mrt_station = spot["MRT"]
        address = spot["address"] # Use address from attractions data
        district = get_district(address) # Use district from attractions data

    # Create a dictionary to store spot information
    spot_info = {
                "id": id,
                "SpotTitle": SpotTitle,
                "District": district,
                "longitude": longitude,
                "latitude": latitude,
                "first_image_url": first_image_url
    }

    # Write the spot information to CSV (or store in a list for further processing)
    writer.writerow(spot_info.values())

print("spot.csv file created successfully!")

'''
#Extract the district data
for spot in mrt_data:
    # Extract address information
    serial_no = spot["SERIAL_NO"]
    mrt_station = spot["MRT"]
    address = spot["address"] # Use address from attractions data
    mrt_district = get_district(address) # Use district from attractions data
    mrt_list = {"MRT": mrt_station, "District": mrt_district, "SERIAL_NO": serial_no}


#Extract the spot data
for spot in spot_data:
    SpotTitle = spot["stitle"]
    longitude = spot["longitude"]
    latitude = spot["latitude"]
    serial_no = spot["SERIAL_NO"]
    info = spot["info"]
    image = spot["filelist"].split("https://www.travel.taipei")

    # Find the first element containing ".JPG" or ".jpg" (case-insensitive)
    first_image_url = None
    for url in image:
        if url.lower().endswith(".jpg"):
            first_image_url = "https://www.travel.taipei" + url
            break
    serial_no_district_spot = mrt_district.get["SERIAL_NO"]
    spot_list = {"SpotTitle": SpotTitle, "District": serial_no_district_spot, "longitude": longitude, "latitude": latitude, "first_image_url": first_image_url}
'''