import requests
from ics import Calendar
from datetime import datetime, timedelta
import re

def get_week_events_from_url(ics_url):
	# fetch the ICS file from the URL
	response = requests.get(ics_url)
	
	# parse the ICS file
	calendar = Calendar(response.text)

	# get today's date
	today = datetime.today()

	# find the next Monday
	days_until_monday = (7 - today.weekday()) % 7
	next_monday = today + timedelta(days=days_until_monday)

	# find the next Sunday
	next_sunday = next_monday + timedelta(days=6)

	# filter events happening between next Monday and Sunday
	week_events = [
		event for event in calendar.events
		if event.begin.date() >= next_monday.date() and event.begin.date() <= next_sunday.date()
	]

	return week_events

def construct_url(event_url):
	course_number = re.search(r'course_[0-9]+', event.url).group()
	course = re.search(r'[0-9]+', course_number).group()

	assignment_number = re.search(r'assignment_[0-9]+', event.url).group()
	assignment = re.search(r'[0-9]+', assignment_number).group()

	return f"https://csusm.instructure.com/courses/{course}/assignments/{assignment}"

url = ""

events = get_week_events_from_url(url)

# print to terminal

print("This weeks homework:")
for event in events:
	print(f" * {event.name}")
	print(f"   Link: {construct_url(event.url)}")

# write to markdown file

with open("output.md", "w") as f:
	f.write("## This weeks homework\n")
	for event in events:
		f.write(f"- [ ] [{event.name}]({event.url})\n\n")