# GTFS-Realtime to Database

The python script loads GTFS-Realtime 2.0 data from your desired agency and store it in a specified database. The GTFS-realtime feed must provide the following information:

* TripUpdates
* VehiclePositions
* Service Alerts

Read more about the GTFS_RT [here](https://developers.google.com/transit/gtfs-realtime)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine or a server for developement and testing purposes.
 
### Prerequisites

1. Below is a list of Python 3 packages required to be installed for this project (these packages are not included as part of Python standard library):

* gtfs-realtime-bindings==0.0.6 (optional - Read BUGS SECTION)
* protobuf==3.9.1 
* sqlalchemy==1.3.7 or sqlalchemy<2.0
    *** The latest version of SQLAlchemy (2.0) has removed Engine.execute. For the time being you may need to downgrade SQLAlchemy***
* pytz==2019.2 
* psycopg2==2.8.3

To install the aforementioned python packages, enter the following command in the command prompt:

```
pip install <Package_name>
```
For example:

pip install sqlalchemy==1.3.7
pip install --user --upgrade "sqlalchemy<2.0"

2. A database - PostgreSQL (PostGIS for Geo tables) - preferred

Download PostgreSQL [here](#https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
Learn how to create a database [here](#https://www.geeksforgeeks.org/postgresql-create-database/)


### Installation
1. Clone or download the project [here](#https://github.com/NewOrleansRTA/GTFSRTDB)
2. Go to the project directory by enter:
```
cd <path_to_the_project>
```
3. Run gtfsrdb.py script (please see the section below for details)


## Usage

### Input List
Following is a list of input available:

* `-t` OR `--trip-updates`: Specify TripUpdates URI
* `-p` OR `--vehicle-positions`: Specify VehiclePositions URI
* `-a` OR `--alerts`: Specify Alerts URI
* `-d` OR `--database`: Specify datavase url
* `-o` OR `--discard-old`: Specify to discard old data to keep the database uptodate
* `-c` OR `--create-tables`: Create tables in the database if not currently exist
* `-w` OR `--wait`: Specify number of seconds before the next request starts
* `-1` OR `--once`: Specify if the request is to be run only once
* `-k` OR `--apikey`: Specify API Key



### Example Use

Links to GTFS-RT

https://YOUR_URL.com/gtfsrt/vehiclePositions
https://YOUR_URL.com/gtfsrt/tripUpdates
https://YOUR_URL.com/gtfsrt/alerts

Database PATH
postgres://[user]:[password]@[host]:[port]/[database]

**Case1:** Load GTFS-realtime bus positions and store it the specified database. The request will run every 30 second (default wait time) and new data will be appended to the table. 

```
python gtfsrtdb.py -p 'https://ULR.com/v2/gtfsrt/vehiclePositions' --database="postgresql+psycopg2://[user]:[password]@[host]:[port]/[database]" --apikey="<Your API Key>" --wait=10 -c

```

```
python gtfsrtdb.py -t=https://ULR.com/v2/gtfsrt/trips' -p=https://ULR.com/v2/gtfsrt/vehicles -a=https://ULR.com/v2/gtfsrt/gtfsrt/alerts --database="postgresql+psycopg2://[user]:[password]@[host]:[port]/[database]" --apikey="<Your API Key>" --wait=10 -c

```

**Case2:** Notice that `-1` is used in this case. The request happens only once querying TripUpdates or any of other feed information to the specified database.

```
python gtfsrtdb.py -t 'https://ULR.com/v2/gtfsrt/tripUpdates' --database="--database="postgresql+psycopg2://[user]:[password]@[host]:[port]/[database]" --apikey="<Your API Key>" -c -1
```

## Output
### Database
Data is stored in table(s) in the specified database. Tables created include:

* alerts
* entity_selectors
* stop_time_updates
* trip_updates
* vehicle_positions

### Logging
Logging will be kept and the default location of the log file can be found in `logs/GTFSR.log`
The location to store log fle can be changed in `logging.conf` under [handler_fileHandler], by modifying the args value.


## Known limitations (BUGS!)

1. The script will not work with the GTFS-RT 1.0.
2. When deploying to Linux server, we encountered an ERROR pertaining the import of the gtfs-realtime-bindings package. *ModuleNotFoundError: No module named 'googletrans'* -- or -- *ModuleNotFoundError: No module named 'google'*. To address the issue, instead of using the  gtfs-realtime-bindings package, use the norta_gtfs_realtime functions and import them into the .py file by commeting and uncommenting the following lines:

#from google.transit import gtfs_realtime_pb2
#import norta_gtfs_realtime_pb2 as gtfs_realtime_pb2



