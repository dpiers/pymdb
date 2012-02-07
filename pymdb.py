import pycurl, random, sys, os, urllib

curl = pycurl.Curl()
outfile = file("output.html", "w")
curl.setopt(pycurl.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)')
curl.setopt(pycurl.WRITEDATA, outfile)

# Returns titleID from movie name
def get_tid(title):
  outfile = file("output.html", "w")
  urlTitle = urllib.quote(title)
  curl.setopt(pycurl.URL, 'http://www.imdb.com/find?s=tt&q=' + urlTitle)
  curl.perform()
  outfile.close()
  infile = file("output.html", "r")
  testLine = """<a href="/title/"""
  for line in infile:
    ar = line.split(testLine)
    if len(ar) > 1:
      title = ar[1].split('/')
      infile.close()
      return title[0]
  return "Failed to grab TitleID!"

# Returns actorID from actor name
def get_aid(name):
  outfile = file("output.html", "w")
  urlName = urllib.quote(name)
  curl.setopt(pycurl.URL, 'http://www.imdb.com/search/name?name=' + urlName)
  curl.perform()
  outfile.close()
  infile = file("output.html", "r")
  testLine = """<a href="/name/"""
  for line in infile:
    ar = line.split(testLine)
    if len(ar) > 1:
      name = ar[1].split('/')
      infile.close()
      return name[0]
  return "Failed to grab ActorID!"

# Returns list of actorIDs from a titleID
def get_actors(titleID):
  outfile = file("output.html", "w") 
  curl.setopt(pycurl.URL, 'http://www.imdb.com/title/' + titleID + '/fullcredits')
  curl.perform()
  outfile.close()
  infile = file("output.html", "r")
  outText = []
  prefixLine = """td class="nm"><a href="""
  testLine = "name"
  for line in infile:
    ar = line.split('/')
    for i in range(len(ar)):
      if testLine == ar[i]:
        if prefixLine in ar[i-1]:
          outText.append( ar[i+1] )
    else:
      continue
  infile.close()
  return outText

# Returns list of movies with actorID
def get_movies(actorID):
  outfile = file("output.html", "w") 
  curl.setopt(pycurl.URL, 'http://www.imdb.com/name/' + actorID + '/filmotype')
  curl.perform()
  outfile.close()
  infile = file("output.html", "r")
  outText = []
  testLine = """<a name="actor_main">Actor:</a></h5>"""
  movieTest = "title"
  for line in infile:
    ar = line.split(testLine)
    if len(ar) > 1:
      actorAr = ar[1].split( "h5" )
      searchAr = actorAr[0].split( '/' )
      for i in range(len(searchAr)):
        if movieTest == searchAr[i]:
            outText.append( searchAr[i+1] )
  return outText

# Returns name of actor from actorID
def get_name(actorID):
  outfile = file("output.html", "w")
  curl.setopt(pycurl.URL, 'http://www.imdb.com/name/' + actorID + '/')
  curl.perform()
  outfile.close()
  infile = file("output.html", "r")
  testLine = """<h1 class="header" itemprop="name">"""
  for line in infile:
    ar = line.split(testLine)
    if len(ar) > 1:
      infile.close()
      return ar[1].strip()
  return "No actor name found"

# Returns name of movie from titleID
def get_title(titleID):
  outfile = file("output.html", "w")
  curl.setopt(pycurl.URL, 'http://www.imdb.com/title/' + titleID + '/' )
  curl.perform()
  outfile.close()
  infile = file("output.html", "r")
  testLine = """<h1 class="header" itemprop="name">"""
  line = infile.readline()
  while line:
    line = infile.readline()
    if line.find(testLine) > -1:
      line = infile.readline()
      infile.close()
      return line.strip()
  return "No movie name found"

# Pick random item in a list
def get_random( inputList ):
  index = 0
  if len(inputList) > 1:
    index = random.randint(0, len(inputList) - 1)
    return inputList[ index ]
  else:
    return inputList[ 0 ]


# Sample usage
while True:
  inputString = raw_input("Format: { t | n }:{ title | name }\n")
  arr = inputString.split(':')

  if arr[0] == "t":
    tid = get_tid( arr[1] )
    print tid
    movieTitle = get_title(tid)
    print "Movie: " + movieTitle
    actors = get_actors(tid)
    print "Actors:"
    print actors
    randomActor = get_random(actors)
    actorName = get_name(randomActor)
    print "Actor: " + actorName
    
  elif arr[0] == "n":
    aid = get_aid( arr[1] )
    print aid
    actorName = get_name(aid)
    print "Actor: " + actorName
    movies = get_movies(aid)
    print "Movies:"
    print movies
    randomMovie = get_random(movies)
    movieName = get_title(randomMovie)
    print "Movie: " + movieName
