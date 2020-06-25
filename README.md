# strava-py
This is a simple project to pull back data from Strava.

It pulls back the last 7, 30, and 90 days of activities of type Ride, VirtualRide, and EBikeRide and shows you your distance, elevation gain, time, and averages.

It is built using Python and uses [stravalib](https://pythonhosted.org/stravalib/) to pull from Strava.

Key features include:
* AWS Lambda
* AWS Lambda Layer to make it prettier
* S3 bucket to host the main web page and graphics
* Amazing graphics (ha, not really)

This uses a AWS Lambda Layer to upload stravalib without cluttering the directory 

From this article
https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17

```
├── lambda_function
└── lambda_layers
    └── python
        └── lib
            └── python3.7
                └── site-packages
└── s3_files
```

Installed stravalib to the structure
```
pip3 install stravalib -t lambda_layers/python/lib/python3.7/site-packages/.
zip -r9 stravalib
cd lambda_layers
zip -r9 stravalib_lambda_layer.zip *
```