import urllib.request
import json
import csv
from datetime import datetime, timezone
import pytz

# Bitcoin Genesis Block Transactions
mlbScheduleUrl = 'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-01-01&endDate=2023-12-31'

venueTimeZones = {
    "American Family Field": 'US/Central',
    "American Family Fields of Phoenix": 'US/Arizona',
    "Angel Stadium": 'US/Pacific',
    "BayCare Ballpark": 'US/Eastern',
    "Busch Stadium": 'US/Central',
    "Camelback Ranch": 'US/Arizona',
    "Chase Field": 'US/Arizona',
    "Citi Field": 'US/Eastern',
    "Citizens Bank Park": 'US/Eastern',
    "Clover Park": 'US/Eastern',
    "Comerica Park": 'US/Eastern',
    "Constellation Field": 'US/Central',
    "CoolToday Park": 'US/Eastern',
    "Coors Field": 'US/Mountain',
    "Dodger Stadium": 'US/Pacific',
    "Ed Smith Stadium": 'US/Eastern',
    "Estadio Alfredo Harp Helu": 'Mexico/General',
    "Fenway Park": 'US/Eastern',
    "George M. Steinbrenner Field": 'US/Eastern',
    "Globe Life Field": 'US/Mountain',
    "Goodyear Ballpark": 'US/Arizona',
    "Great American Ball Park": 'US/Eastern',
    "Guaranteed Rate Field": 'US/Central',
    "Hammond Stadium": 'US/Eastern',
    "Hohokam Stadium": 'US/Arizona',
    "JetBlue Park": 'US/Eastern',
    "Kauffman Stadium": 'US/Central',
    "Las Vegas Ballpark": 'US/Pacific',
    "LECOM Park": 'US/Eastern',
    "loanDepot park": 'US/Eastern',
    "London Stadium": 'GB',
    "Minute Maid Park": 'US/Mountain',
    "Muncy Bank Ballpark": 'US/Eastern',
    "Nationals Park": 'US/Eastern',
    "Oakland Coliseum": 'US/Pacific',
    "Oracle Park": 'US/Pacific',
    "Oriole Park at Camden Yards": 'US/Eastern',
    "Peoria Stadium": 'US/Arizona',
    "Petco Park": 'US/Pacific',
    "PNC Park": 'US/Eastern',
    "Progressive Field": 'US/Eastern',
    "Publix Field at Joker Marchant Stadium": 'US/Eastern',
    "Roger Dean Chevrolet Stadium": 'US/Eastern',
    "Rogers Centre": 'Canada/Eastern',
    "Salt River Fields at Talking Stick": 'US/Arizona',
    "Scottsdale Stadium": 'US/Arizona',
    "Sloan Park": 'US/Arizona',
    "Surprise Stadium": 'US/Arizona',
    "Target Field": 'US/Central',
    "TD Ballpark": 'US/Eastern',
    "Tempe Diablo Stadium": 'US/Arizona',
    "The Ballpark of the Palm Beaches": 'US/Eastern',
    "The Stadium at the ESPN Wide World of Sports": 'US/Eastern',
    "T-Mobile Park": 'US/Pacific',
    "Tropicana Field": 'US/Eastern',
    "Truist Park": 'US/Eastern',
    "Wrigley Field": 'US/Central',
    "Yankee Stadium": 'US/Eastern'
}

with urllib.request.urlopen(mlbScheduleUrl) as urlStream:
    schedule = json.loads(urlStream.read().decode())
    dates = schedule['dates']
    
    with open('MLBSchedule.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(['UTC', 'Date', 'Local', 'Away', 'Home', 'Venue', 'TZ', 'Description'])
        for date in dates:
            for game in date['games']:
                teams = game['teams']
                venue = game['venue']['name']
                timeZoneLocal = pytz.timezone(venueTimeZones[venue])
                dateTimeUTC = datetime.fromisoformat(game['gameDate'][:-1] + '+00:00')
                dateTimeLocal = dateTimeUTC.astimezone(timeZoneLocal)
                writer.writerow([dateTimeUTC.isoformat(), dateTimeLocal.date(), dateTimeLocal.time().strftime("%I:%M %p"), teams['away']['team']['name'], teams['home']['team']['name'], venue, timeZoneLocal, game['seriesDescription']])