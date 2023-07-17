import os
from api.ssmpd import ssmpdAPI

# get number of endpoints
ENDPOINTS = os.getenv('ENDPOINTS')

# create new object
app = ssmpdAPI('0.0.0.0', 8080)

# run it
if __name__ == '__main__':
    app.run()
