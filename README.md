# strava-py
This is a simple project to pull back data from Strava.

It pulls back the last 7, 30, and 90 days of activities and shows you your distance, elevation gain, time, and averages.

It is built using Python and uses [stravalib](https://pythonhosted.org/stravalib/) to pull from Strava.

Key features include:
* Local version (recents.py and recents2.py) for testing purposes
* AWS Lambda (recentLambda.py and recentLambdaThree.py) versions

TODO
Use AWS Lambda Layers to clean up the mess of folders and runtimes
