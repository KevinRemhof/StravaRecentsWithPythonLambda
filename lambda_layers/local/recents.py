#!/usr/local/bin/python3
import http.server
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
        return round(self.elevation / self.distance)

    def miles_per_day(self):
        return round(self.distance / self.days)

    def time_per_day(self):
        return round(self.minutes / self.days)
    
def PrintNewTotals(rides):
    print(rides)
    #print('Title=' + rides.title)
    #print('Days=' + str(rides.days))
    #print('Count=' + str(rides.count))
    #print('Distance=' + str(rides.distance))
    #print('Elevation=' + str(rides.elevation))
    #print('Minutes=' + str(rides.minutes))
    #print('Eddington=' + str(rides.eddington))
    #print('Feet per Mile=' + str(rides.feet_per_mile()))
    #print('Miles per Day=' + str(rides.miles_per_day()))
    #print('Time per Day=' + str(rides.time_per_day()))
    #print()

def GetTotalsForDays(title, daysBack, activities):
    allCount = 0
    allDistance = 0
    allElevation = 0
    allTime = 0

    fromdate = datetime.datetime.now() + datetime.timedelta(daysBack * -1)

    rideLengths = []

    for activity in activities:
        #Adding date restriction
        if activity.start_date_local > fromdate:
            allCount += 1
            allDistance += activity.distance.num
            allElevation += activity.total_elevation_gain.num
            allTime += int(activity.moving_time.seconds)
            rideLengths.append(getMiles(activity.distance.num))

    allEddington = getEddington(rideLengths)
    allDistanceInMiles = getMiles(allDistance)
    allElevationInFeet = getFeet(allElevation)
    allTimeInMinutes = round(allTime / 60)

    return RideTotals(title,daysBack,allCount,allDistanceInMiles,allElevationInFeet,allTimeInMinutes,allEddington)

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

def BuildRow(rideTotals):
    outputHtml = '<tr>'
    outputHtml += '<td>' + rideTotals.title + '</td>'
    outputHtml += '<td>' + f'{rideTotals.count:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.distance:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.elevation:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.minutes:,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.feet_per_mile():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.miles_per_day():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.time_per_day():,}' + '</td>'
    outputHtml += '<td>' + f'{rideTotals.eddington:,}' + '</td>'
    outputHtml += '</tr>'
    return outputHtml

def GetTotals(daysBack, client):
    #Retrieve the last x days of activities
    fromdate = datetime.datetime.now() + datetime.timedelta(daysBack * -1)

    activities = GetActivitiesFromDate(client,fromdate)

    allCount = 0
    allDistance = 0
    allElevation = 0
    allTime = 0

    rideLengths = []

    for activity in activities:
        allCount += 1
        allDistance += activity.distance.num
        allElevation += activity.total_elevation_gain.num
        allTime += int(activity.moving_time.seconds)
        rideLengths.append(getMiles(activity.distance.num))

    allEddington = getEddington(rideLengths)
    allDistanceInMiles = getMiles(allDistance)
    allElevationInFeet = getFeet(allElevation)
    allFeetPerMile = round(allElevationInFeet / allDistanceInMiles)
    allMilesPerDay = round(allDistanceInMiles / daysBack)
    allTimeInMinutes = round(allTime / 60)
    allTimePerDay = round((allTime / daysBack) / 60)

    print('Last ' + f'{daysBack:,}' + ' Days')
    print('Rides: ', allCount)
    print('Distance: ', allDistanceInMiles)
    print('Elevation: ', allElevationInFeet)
    print()

    outputHtml = '<tr>'
    outputHtml += '<td>' + f'{daysBack:,}' + '</td>'
    outputHtml += '<td>' + f'{allCount:,}' + '</td>'
    outputHtml += '<td>' + f'{allDistanceInMiles:,}' + '</td>'
    outputHtml += '<td>' + f'{allElevationInFeet:,}' + '</td>'
    outputHtml += '<td>' + f'{allTimeInMinutes:,}' + '</td>'
    outputHtml += '<td>' + f'{allFeetPerMile:,}' + '</td>'
    outputHtml += '<td>' + f'{allMilesPerDay:,}' + '</td>'
    outputHtml += '<td>' + f'{allTimePerDay:,}' + '</td>'
    outputHtml += '<td>' + f'{allEddington:,}' + '</td>'
    outputHtml += '</tr>'

    return outputHtml

def GetTotalsYTD(client):
    #Retrieve year to date activities
    currDate = datetime.datetime.now()
    currYear = currDate.year
    fromDate = datetime.datetime(currYear, 1, 1)
    dayOfYear = currDate.timetuple().tm_yday

    activities = GetActivitiesFromDate(client,fromDate)

    allCount = 0
    allDistance = 0
    allElevation = 0
    allTime = 0

    rideLengths = []

    for activity in activities:
        allCount += 1
        allDistance += activity.distance.num
        allElevation += activity.total_elevation_gain.num
        allTime += int(activity.moving_time.seconds)
        rideLengths.append(getMiles(activity.distance.num))

    allEddington = getEddington(rideLengths)
    allDistanceInMiles = getMiles(allDistance)
    allElevationInFeet = getFeet(allElevation)
    allFeetPerMile = round(allElevationInFeet / allDistanceInMiles)
    allMilesPerDay = round(allDistanceInMiles / dayOfYear)
    allTimeInMinutes = round(allTime / 60)
    allTimePerDay = round((allTime / dayOfYear) / 60)

    print('Year to Date')
    print('Rides: ', allCount)
    print('Distance: ', allDistanceInMiles)
    print('Elevation: ', allElevationInFeet)
    print()

    outputHtml = '<tr>'
    outputHtml += '<td>Year to Date (Day ' + f'{dayOfYear:,}' + ')</td>'
    outputHtml += '<td>' + f'{allCount:,}' + '</td>'
    outputHtml += '<td>' + f'{allDistanceInMiles:,}' + '</td>'
    outputHtml += '<td>' + f'{allElevationInFeet:,}' + '</td>'
    outputHtml += '<td>' + f'{allTimeInMinutes:,}' + '</td>'
    outputHtml += '<td>' + f'{allFeetPerMile:,}' + '</td>'
    outputHtml += '<td>' + f'{allMilesPerDay:,}' + '</td>'
    outputHtml += '<td>' + f'{allTimePerDay:,}' + '</td>'
    outputHtml += '<td>' + f'{allEddington:,}' + '</td>'
    outputHtml += '</tr>'

    return outputHtml

# This class will handles any incoming request from
# the browser
class myHandler(http.server.BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        #Get the API code for Strava
        try:
            code = parse_qs(urlparse(self.path).query)['code'][0]
        except:
            print('No code on URL')
            return

        #Login to the API and get the Athlete
        client,athlete = GetClient(code)

        outputHtml = '<!DOCTYPE html>'
        outputHtml += '<html>'
        outputHtml += '<head>'
        outputHtml += '<style>'
        outputHtml += '#customers {'
        outputHtml += '  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;'
        outputHtml += '  border-collapse: collapse;'
        outputHtml += '  width: 100%;'
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
        outputHtml += '<body>'

        outputHtml += '<h1>Hello, ' + str(athlete.firstname) + '</h1>'
        outputHtml += '<h2>Here are your recent stats from Strava</h2>'
        
        outputHtml += '<table id="customers">'

        outputHtml += '<tr>'
        outputHtml += '<th>Days</th>'
        outputHtml += '<th>Rides</th>'
        outputHtml += '<th>Distance (Miles)</th>'
        outputHtml += '<th>Elevation (Feet)</th>'
        outputHtml += '<th>Moving Time (Minutes)</th>'
        outputHtml += '<th>Feet per Mile</th>'
        outputHtml += '<th>Miles per Day</th>'
        outputHtml += '<th>Minutes per Day</th>'
        outputHtml += '<th>Eddington</th>'
        #outputHtml += '<th>Time</th>'
        outputHtml += '</tr>'

        activities = GetActivitiesFromDaysBack(client,365)

        seven,thirty,ninety,oneeighty,threesixtyfive,yeartodate = GetTotalsForMultipleDays(activities)

        PrintNewTotals(seven)
        PrintNewTotals(thirty)
        PrintNewTotals(ninety)
        PrintNewTotals(oneeighty)
        PrintNewTotals(threesixtyfive)
        PrintNewTotals(yeartodate)

        outputHtml += BuildRow(seven)
        outputHtml += BuildRow(thirty)
        outputHtml += BuildRow(ninety)
        outputHtml += BuildRow(oneeighty)
        outputHtml += BuildRow(threesixtyfive)
        outputHtml += BuildRow(yeartodate)

        outputHtml += '</table>'
        outputHtml += '</body>'
        outputHtml += '</html>'
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Send the html message
        self.wfile.write(outputHtml.encode(encoding='utf_8'))

        return

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = http.server.HTTPServer(('', port_number), myHandler)
    print('Started httpserver on port ', port_number)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()