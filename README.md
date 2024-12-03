# Virtual Environment

    source ./final/bin/activate

# Converting Garmin FIT to CSV 

First, install `fitparse`

    sudo pip3 install -e git+https://github.com/dtcooper/python-fitparse#egg=python-fitparse

OR

    sudo pip3 install fitparse

Then you can execute 

    python3 fit_to_csv.py

This will create a bunch of CSVs for all of your workouts in that directory (You will be asked to enter the directory in terminal after running fit_to_csv.py). The files will be stored in the directory you designate. 
