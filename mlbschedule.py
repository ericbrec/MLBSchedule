import urllib.request
import json
import csv
from datetime import datetime, timezone
import pytz

year = 2025
mlbScheduleUrl = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={year}-01-01&endDate={year}-12-31"

venueTimeZones = {
    "American Family Field": 'US/Central',
    "American Family Fields of Phoenix": 'US/Arizona',
    "Angel Stadium": 'US/Pacific',
    "Arvest Ballpark": 'US/Central',
    "AutoZone Park": 'US/Central',
    "BayCare Ballpark": 'US/Eastern',
    "Bristol Motor Speedway": 'US/Eastern',
    "Busch Stadium": 'US/Central',
    "CACTI Park of the Palm Beaches": 'US/Eastern',
    "Camelback Ranch": 'US/Arizona',
    "Charlotte Sports Park": 'US/Eastern',
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
    "Estadio Quisqueya Juan Marichal": 'America/Santo_Domingo',
    "Fenway Park": 'US/Eastern',
    "George M. Steinbrenner Field": 'US/Eastern',
    "Globe Life Field": 'US/Mountain',
    "Gocheok Sky Dome": 'Asia/Seoul',
    "Goodyear Ballpark": 'US/Arizona',
    "Great American Ball Park": 'US/Eastern',
    "Guaranteed Rate Field": 'US/Central',
    "Hammond Stadium": 'US/Eastern',
    "Hohokam Stadium": 'US/Arizona',
    "JetBlue Park": 'US/Eastern',
    "Journey Bank Ballpark": 'US/Eastern',
    "Kauffman Stadium": 'US/Central',
    "Las Vegas Ballpark": 'US/Pacific',
    "LECOM Park": 'US/Eastern',
    "Lee Health Sports Complex": 'US/Eastern',
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
    "Rickwood Field": 'US/Central',
    "Roger Dean Chevrolet Stadium": 'US/Eastern',
    "Rogers Centre": 'Canada/Eastern',
    "Salt River Fields at Talking Stick": 'US/Arizona',
    "Scottsdale Stadium": 'US/Arizona',
    "Sloan Park": 'US/Arizona',
    "Surprise Stadium": 'US/Arizona',
    "Sutter Health Park": 'US/Pacific',
    "Target Field": 'US/Central',
    "TD Ballpark": 'US/Eastern',
    "Tempe Diablo Stadium": 'US/Arizona',
    "The Ballpark of the Palm Beaches": 'US/Eastern',
    "The Stadium at the ESPN Wide World of Sports": 'US/Eastern',
    "T-Mobile Park": 'US/Pacific',
    "Tokyo Dome": 'Asia/Tokyo',
    "Tropicana Field": 'US/Eastern',
    "Truist Park": 'US/Eastern',
    "Wrigley Field": 'US/Central',
    "Yankee Stadium": 'US/Eastern'
}

#print(' '.join(pytz.country_timezones['kr']))

with urllib.request.urlopen(mlbScheduleUrl) as urlStream:
    schedule = json.loads(urlStream.read().decode())
    dates = schedule['dates']
    
    with open('MLBSchedule.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(['Date', 'Time', 'Away', 'Home', 'Venue', 'TZ', 'Description'])
        for date in dates:
            for game in date['games']:
                teams = game['teams']
                venue = game['venue']['name']
                timeZoneLocal = pytz.timezone(venueTimeZones[venue])
                dateTimeUTC = datetime.fromisoformat(game['gameDate'][:-1] + '+00:00')
                dateTimeLocal = dateTimeUTC.astimezone(timeZoneLocal)
                writer.writerow([dateTimeLocal.date(), dateTimeLocal.time().strftime("%I:%M %p"), teams['away']['team']['name'], teams['home']['team']['name'], venue, timeZoneLocal, game['seriesDescription']])