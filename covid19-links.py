import re
import requests
import webbrowser

# base content, from https://github.com/auino/covid19-links
URL = "https://raw.githubusercontent.com/auino/covid19-links/master/README.md"

# how many '#' characters to identify the sections to filter in?
FILTERS_TAGCOUNT = 4
# which sections to filter in?
FILTERS_ELEMENTS = ['World', 'Italy', 'Liguria']

# returns if s is a header or not
def isheader(s): return s.startswith('#')

# retrieves the beginning of the header tag from an input title
def getfiltertag(s=None):
	filter_tag = ''
	for i in range(0, FILTERS_TAGCOUNT): filter_tag +='#'
	if s != None: filter_tag+=' '+s
	return filter_tag

# returns if a string is inside of a filter or not
def isinfilter(s):
	for f in FILTERS_ELEMENTS:
		if s.startswith(getfiltertag(f)): return True
	return False

# get all links found in s
def getlinks(s):
	res = []
	r = re.finditer(r'\((.*?)\)', s)
	for x in r:
		u = x.group(0)[1:-1]
		res.append(u)
	return res

# getting the content
t = requests.get(URL).text

# variable to discriminate filtered content
link_in_filter = False
# cycling on all the lines of the base file
for l in t.split('\n'):
	# checking if the current line is a header
	if isheader(l):
		# checking if the current header in in the list of filtered headers or not
		link_in_filter = isinfilter(l)
		continue
	# filtering out all not needed content
	if not link_in_filter: continue
	# getting links to show, for filtered in content
	for u in getlinks(l):
		print(u)
		webbrowser.open_new_tab(u)
