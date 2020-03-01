#!/usr/local/bin/python3
from urllib.parse import urlparse
from urllib.parse import parse_qs
import stravalib
import datetime
from dataclasses import dataclass

#Global Variables - Create a file called 'client.secret.txt' and put in the 'Client ID' and 'Your Access Token' from https://www.strava.com/settings/api
#client_id,your_access_token
client_id, secret = open('client.secret.txt').read().strip().split(',')
port_number = 5000
#url = 'http://localhost:%d/authorized' % port
#allDone = False
types = ['time', 'distance', 'latlng', 'altitude', 'velocity_smooth', 'moving', 'grade_smooth', 'temp']
limit = 10
client = stravalib.client.Client()

def GetClient(code):
    #Retrieve the login code from the Strava server
    token_response = client.exchange_code_for_token(client_id, secret, code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']

    #Store the access token somewhere (right now it is just a local variable)
    client.access_token = access_token
    client.refresh_access_token = refresh_token
    #TODO do something with the expiration token
        
    #Grab the athlete number for logging purposes
    athlete = client.get_athlete()

    strExpires = datetime.datetime.fromtimestamp(expires_at).strftime('%Y-%m-%d %H:%M:%S')

    print('For %(first)s %(last)s (%(id)s), I now have access token %(token)s which expires at %(expires)s' %
            {'first': athlete.firstname, 'last': athlete.lastname, 'id': athlete.id, 'token': access_token, 'expires': strExpires})

    return client,athlete

def GetActivitiesFromDaysBack(client, daysBack):
    fromdate = datetime.datetime.now() + datetime.timedelta(daysBack * -1)

    activities = client.get_activities(after=fromdate)
    return activities

def GetActivitiesFromDate(client, fromdate):
    activities = client.get_activities(after=fromdate)
    return activities

def getMiles(distance):
    return round(distance * 0.000621371192)

def getFeet(elevation):
    return round(elevation * 3.28084)

def getEddington(rides) -> int:
    if not rides:
        return 0

    for E, ride in enumerate(sorted(rides, reverse=True), 1):
        if ride < E:
            E -= 1
            break

    return E

@dataclass
class RideTotals:
    title : str
    days: int
    count: int
    distance: int
    elevation: int
    minutes: int
    eddington : int

    def feet_per_mile(self):
        return round(self.elevation / self.distance) if self.distance else 0

    def miles_per_day(self):
        return round(self.distance / self.days) if self.days else 0

    def time_per_day(self):
        return round(self.minutes / self.days) if self.days else 0
    
def GetTotalsForMultipleDays(activities):
    sevenCount = 0
    sevenDistance = 0
    sevenElevation = 0
    sevenTime = 0
    sevenDate = datetime.datetime.now() + datetime.timedelta(7 * -1)
    sevenRideLengths = []

    thirtyCount = 0
    thirtyDistance = 0
    thirtyElevation = 0
    thirtyTime = 0
    thirtyDate = datetime.datetime.now() + datetime.timedelta(30 * -1)
    thirtyRideLengths = []

    ninetyCount = 0
    ninetyDistance = 0
    ninetyElevation = 0
    ninetyTime = 0
    ninetyDate = datetime.datetime.now() + datetime.timedelta(90 * -1)
    ninetyRideLengths = []

    oneeightyCount = 0
    oneeightyDistance = 0
    oneeightyElevation = 0
    oneeightyTime = 0
    oneeightyDate = datetime.datetime.now() + datetime.timedelta(180 * -1)
    oneeightyRideLengths = []

    threesixtyfiveCount = 0
    threesixtyfiveDistance = 0
    threesixtyfiveElevation = 0
    threesixtyfiveTime = 0
    threesixtyfiveDate = datetime.datetime.now() + datetime.timedelta(365 * -1)
    threesixtyfiveRideLengths = []

    ytdCount = 0
    ytdDistance = 0
    ytdElevation = 0
    ytdTime = 0
    #TODO make this the actual YTD
    currDate = datetime.datetime.now()
    currYear = currDate.year
    ytdDate = datetime.datetime(currYear, 1, 1)
    ytdDayOfYear = currDate.timetuple().tm_yday


    ytdRideLengths = []

    for activity in activities:
        if activity.type in (activity.RIDE, activity.VIRTUALRIDE, activity.EBIKERIDE):
            if activity.start_date_local > sevenDate:
                sevenCount += 1
                sevenDistance += activity.distance.num
                sevenElevation += activity.total_elevation_gain.num
                sevenTime += int(activity.moving_time.seconds)
                sevenRideLengths.append(getMiles(activity.distance.num))
            if activity.start_date_local > thirtyDate:
                thirtyCount += 1
                thirtyDistance += activity.distance.num
                thirtyElevation += activity.total_elevation_gain.num
                thirtyTime += int(activity.moving_time.seconds)
                thirtyRideLengths.append(getMiles(activity.distance.num))
            if activity.start_date_local > ninetyDate:
                ninetyCount += 1
                ninetyDistance += activity.distance.num
                ninetyElevation += activity.total_elevation_gain.num
                ninetyTime += int(activity.moving_time.seconds)
                ninetyRideLengths.append(getMiles(activity.distance.num))
            if activity.start_date_local > oneeightyDate:
                oneeightyCount += 1
                oneeightyDistance += activity.distance.num
                oneeightyElevation += activity.total_elevation_gain.num
                oneeightyTime += int(activity.moving_time.seconds)
                oneeightyRideLengths.append(getMiles(activity.distance.num))
            if activity.start_date_local > threesixtyfiveDate:
                threesixtyfiveCount += 1
                threesixtyfiveDistance += activity.distance.num
                threesixtyfiveElevation += activity.total_elevation_gain.num
                threesixtyfiveTime += int(activity.moving_time.seconds)
                threesixtyfiveRideLengths.append(getMiles(activity.distance.num))
            if activity.start_date_local > ytdDate:
                ytdCount += 1
                ytdDistance += activity.distance.num
                ytdElevation += activity.total_elevation_gain.num
                ytdTime += int(activity.moving_time.seconds)
                ytdRideLengths.append(getMiles(activity.distance.num))

    sevenEddington = getEddington(sevenRideLengths)
    sevenDistanceInMiles = getMiles(sevenDistance)
    sevenElevationInFeet = getFeet(sevenElevation)
    sevenTimeInMinutes = round(sevenTime / 60)

    thirtyEddington = getEddington(thirtyRideLengths)
    thirtyDistanceInMiles = getMiles(thirtyDistance)
    thirtyElevationInFeet = getFeet(thirtyElevation)
    thirtyTimeInMinutes = round(thirtyTime / 60)

    ninetyEddington = getEddington(ninetyRideLengths)
    ninetyDistanceInMiles = getMiles(ninetyDistance)
    ninetyElevationInFeet = getFeet(ninetyElevation)
    ninetyTimeInMinutes = round(ninetyTime / 60)

    oneeightyEddington = getEddington(oneeightyRideLengths)
    oneeightyDistanceInMiles = getMiles(oneeightyDistance)
    oneeightyElevationInFeet = getFeet(oneeightyElevation)
    oneeightyTimeInMinutes = round(oneeightyTime / 60)

    threesixtyfiveEddington = getEddington(threesixtyfiveRideLengths)
    threesixtyfiveDistanceInMiles = getMiles(threesixtyfiveDistance)
    threesixtyfiveElevationInFeet = getFeet(threesixtyfiveElevation)
    threesixtyfiveTimeInMinutes = round(threesixtyfiveTime / 60)

    ytdEddington = getEddington(ytdRideLengths)
    ytdDistanceInMiles = getMiles(ytdDistance)
    ytdElevationInFeet = getFeet(ytdElevation)
    ytdTimeInMinutes = round(ytdTime / 60)

    #Note: the final return is year to date which uses a different title
    return RideTotals('7',7,sevenCount,sevenDistanceInMiles,sevenElevationInFeet,sevenTimeInMinutes,sevenEddington),RideTotals('30',30,thirtyCount,thirtyDistanceInMiles,thirtyElevationInFeet,thirtyTimeInMinutes,thirtyEddington),RideTotals('90',90,ninetyCount,ninetyDistanceInMiles,ninetyElevationInFeet,ninetyTimeInMinutes,ninetyEddington),RideTotals('180',180,oneeightyCount,oneeightyDistanceInMiles,oneeightyElevationInFeet,oneeightyTimeInMinutes,oneeightyEddington),RideTotals('365',365,threesixtyfiveCount,threesixtyfiveDistanceInMiles,threesixtyfiveElevationInFeet,threesixtyfiveTimeInMinutes,threesixtyfiveEddington),RideTotals('Year to Date (Day ' + str(ytdDayOfYear) + ')',ytdDayOfYear,ytdCount,ytdDistanceInMiles,ytdElevationInFeet,ytdTimeInMinutes,ytdEddington)

def buildHead():
    outputHtml = '<head>'

    outputHtml += '<meta charset="utf-8">'
    outputHtml += '<title>Killer B\'s Recent Strava Stats</title>'
    outputHtml += '<meta name="viewport" content="width=device-width, initial-scale=1">'
    outputHtml += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">'
    outputHtml += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>'
    outputHtml += '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>'
    outputHtml += '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>'

    outputHtml += '<style>'
    outputHtml += '#customers {'
    outputHtml += '  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;'
    outputHtml += '  border-collapse: collapse;'
    #outputHtml += '  width: 100%;'
    outputHtml += '}'

    outputHtml += 'h1 {'
    outputHtml += '  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;'
    outputHtml += '}'

    outputHtml += 'h2 {'
    outputHtml += '  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;'
    outputHtml += '}'

    outputHtml += 'p {'
    outputHtml += '  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;'
    outputHtml += '}'

    outputHtml += 'img.a {'
    outputHtml += '  vertical-align: text-top;'
    outputHtml += '}'

    outputHtml += '#customers td, #customers th {'
    outputHtml += '  border: 1px solid #ddd;'
    outputHtml += '  padding: 8px;'
    outputHtml += '}'

    outputHtml += '#customers tr:nth-child(even){background-color: #f2f2f2;}'

    outputHtml += '#customers tr:hover {background-color: #ddd;}'

    outputHtml += '#customers th {'
    outputHtml += '  padding-top: 12px;'
    outputHtml += '  padding-bottom: 12px;'
    outputHtml += '  text-align: left;'
    outputHtml += '  background-color: #fc4c02;'
    outputHtml += '  color: white;'
    outputHtml += '}'
    outputHtml += '</style>'
    outputHtml += '</head>'

    return outputHtml

def buildStatsTableThree(rideTotals1, rideTotals2, rideTotals3):
    outputHtml = '<table id="customers">'

    outputHtml += '<tr>'
    outputHtml += '<th>Days</th>'
    outputHtml += '<th>' + rideTotals1.title + '</th>'
    outputHtml += '<th>' + rideTotals2.title + '</th>'
    outputHtml += '<th>' + rideTotals3.title + '</th>'
    outputHtml += '</tr>'

    outputHtml += '<tr>'
    outputHtml += '<td>Miles</td>'
    outputHtml += '<td>' + f'{rideTotals1.distance:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals2.distance:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals3.distance:,}' + '</td>'
    outputHtml += '</tr>'
    outputHtml += '<tr>'
    outputHtml += '<td>Feet</td>'
    outputHtml += '<td>' + f'{rideTotals1.elevation:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals2.elevation:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals3.elevation:,}' + '</td>'
    outputHtml += '</tr>'
    outputHtml += '<tr>'
    outputHtml += '<td>Minutes</td>'
    outputHtml += '<td>' + f'{rideTotals1.minutes:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals2.minutes:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals3.minutes:,}' + '</td>'
    outputHtml += '</tr>'
    outputHtml += '<tr>'
    outputHtml += '<td>Miles/day</td>'
    outputHtml += '<td>' + f'{rideTotals1.miles_per_day():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals2.miles_per_day():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals3.miles_per_day():,}' + '</td>'
    outputHtml += '</tr>'
    outputHtml += '<tr>'
    outputHtml += '<td>Feet/mile</td>'
    outputHtml += '<td>' + f'{rideTotals1.feet_per_mile():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals2.feet_per_mile():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals3.feet_per_mile():,}' + '</td>'
    outputHtml += '</tr>'
    outputHtml += '<tr>'
    outputHtml += '<td>Minutes/day</td>'
    outputHtml += '<td>' + f'{rideTotals1.time_per_day():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals2.time_per_day():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals3.time_per_day():,}' + '</td>'
    outputHtml += '</tr>'

    outputHtml += '</table>'

    return outputHtml

def lambda_handler(event, context):
    #Get the API code for Strava
    try:
        operation = event['httpMethod']
        print('Method=' + operation)
        #code = parse_qs(urlparse(self.path).query)['code'][0]
        code = event['queryStringParameters']['code']
        print('The code is ' + code)
    except:
        print('No code on URL')
        print(event)
        return

    #Login to the API and get the Athlete
    client,athlete = GetClient(code)

    outputHtml = '<!DOCTYPE html>'
    outputHtml += '<html lang="en">'
    outputHtml += buildHead()
    outputHtml += '<body>'

    #Top Navigation
    outputHtml += '<nav class="navbar navbar-dark bg-dark">'
    outputHtml += '        <div class="container-fluid">'
    outputHtml += '            <div class="navbar-header">'
    outputHtml += '                <a class="navbar-brand" href="#">'
    outputHtml += '                    <img src="https://s3.amazonaws.com/killerbs.bike/KillerBs.svg" height="50" alt="" class="d-inline-block align-middle mr-2">'
    outputHtml += '                </a>'
    outputHtml += '            </div>'
    outputHtml += '            <ul class="nav navbar-nav navbar-right">'
    outputHtml += '                <li>'
    outputHtml += '                    <a href="#"><span class="glyphicon glyphicon-log-in"></span>'
    outputHtml += '                        <img src="https://s3.amazonaws.com/killerbs.bike/api_logo_pwrdBy_strava_stack_light.svg"'
    outputHtml += '                            height="50" alt="" class="d-inline-block align-middle mr-2">'
    outputHtml += '                    </a>'
    outputHtml += '                </li>'
    outputHtml += '            </ul>'
    outputHtml += '        </div>'
    outputHtml += '    </nav>'
    outputHtml += '<br />'

    outputHtml += '<div class="container">'
    outputHtml += '<h1>Hello, ' + str(athlete.firstname) + ' <img class="a" src="' + str(athlete.profile_medium) + '"></h1>'
    outputHtml += '<h2>Here are your ride (including virtual and eBike) stats for the last 7, 30, and 90 days</h2>'
    
    activities = GetActivitiesFromDaysBack(client,90)

    seven,thirty,ninety,oneeighty,threesixtyfive,yeartodate = GetTotalsForMultipleDays(activities)

    print(seven)
    print(thirty)
    print(ninety)
    
    outputHtml += buildStatsTableThree(seven,thirty,ninety)
    outputHtml += '</div>'
    outputHtml += '</body>'
    outputHtml += '</html>'
    
    return {
        'statusCode': '200',
        'body': outputHtml,
        'headers': {
            'Content-Type': 'text/html',
        },
    }