import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = 'XXXXXXXXXXXXXXXX'	# Enter "Google Places API Key" Here (https://developers.google.com/maps/documentation/geocoding/intro)
serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

conn = sqlite3.connect('GeoData.sqlite')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("GeoData.data")
count = 0
for line in fh:
    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (memoryview(address.encode()), ))

    try:
        data = cur.fetchone()[0]
        print("Found in database ",address)
        continue
    except:
        pass

    parms = dict()
    parms["address"] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving...')
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    #print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        js = json.loads(data)
    except:
        print(data)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failed To Retrieve ====')
        print(data)
        break

    cur.execute("INSERT INTO Locations (address, geodata) VALUES ( ?, ? )", (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()
    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print("Run GeoData_Dump.py to read the data from the database")
