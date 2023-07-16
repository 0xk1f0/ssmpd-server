import os
from ssmpd import ssmpdAPI

# get number of endpoints
ENDPOINTS = os.getenv('ENDPOINTS')

# create new object
app = ssmpdAPI('172.17.2.41', 1704)

# run it
if __name__ == '__main__':
    app.run()
