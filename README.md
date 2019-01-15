# GeoData Project Using Google API
# GeoData.data

Users can add locations in this file for which geocodes are to be downloaded.

# GeoData.sqlite

It is a database to store all the geocodes.

# GeoData_Load.py

It downloads into the database "GeoData.sqlite" the geocodes of the locations indicated in "GeoData.data". Note that in order to download geocodes from Google API, user will require a "Google Places API Key".

# GeoData_Dump.py

It dumps the data to "GeoData.js"

# GeoData.js

It is the JavaScript responsible for the background behaviour of the webpage displayed by "GeoData.html"

# GeoData.html

It is a webpage that shows a "Development Purpose Only" version of Google Maps with all the location pinned.
