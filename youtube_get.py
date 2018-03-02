import sys
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import pafy
import fnmatch
from random import randint

#TODO: make it work with youtube suggestions, weed out results that aren't songs
def get_urls(textToSearch):
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    output_arr = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if len(vid['href']) == 20:
            output_arr.append(vid['href'])
    return output_arr
def search_download(query):
    url = get_urls(query)[0]
    download_song(url)
def meets_standard(video_id):
    #maybe add more stuff to standard
    full_url = "https://youtube.com" + video_id
    new = pafy.new(full_url)
    dur = new.length
    #mid_hun = int(new.duration[1])
    return (dur < 510)
    #return True
def download_song(video_id):
    return os.system('youtube-dl -x "' + "https://youtube.com" + video_id + '"  --audio-format mp3 --audio-quality 0')
def get_mp3_count():
    #returns the number of mp3 files in current folder
    files = os.listdir('.')
    pattern = "*.mp3"
    op_list = []
    for entry in files:
        if fnmatch.fnmatch(entry, pattern):
            op_list.append(entry)
    return len(op_list)
def get_criteria_song(search_arr):
    #this method downloads a song randomly from the search array
    #search_arr is a string array of all the different search criteria strings
    #for example ['Frank Ocean-A', 'Kendrick Lamar-A', 'Good Kid Mad City-Al', 'Blonde-Al', 'Endless-Al', 'MAAD City-S']
    rand = randint(0, len(search_arr) - 2) #picks a random index
    print("search criteria: " + search_arr[rand])
    spl = search_arr[rand].split('$-')
    second = spl[1]
    url_list = get_urls(spl[0])
    url_rand = 0
    if spl[1] == "S":
        url_rand = diligence(url_list, 9)#picks a random video within first 10 results
    elif spl[1] == "Al":
        url_rand = diligence(url_list, 15)#picks a random video within first 10 results
    elif spl[1] == "A":
        url_rand = diligence(url_list, 20)#picks a random video within first 10 results

    #use_url = url_list[url_rand]
    download_song(url_rand)
def diligence(url_list, low):
    print("running")
    picked = ""
    while picked == "":
        url_rand = randint(0, min(low, len(url_list) - 1))
        url_rand = url_list[url_rand]
        if meets_standard(url_rand):
            picked = url_rand

    return picked
def get_text_file_list():
    file_object = open("library_list.txt", "r")
    read = file_object.read()
    spl = read.split('\n')
    return spl
def fill_out_library():
    #get this method to incorporate text files
    search_criteria = get_text_file_list()
    songs_necessary = 100 - get_mp3_count()
    print(str(songs_necessary) + " songs needed")
    for i in xrange(songs_necessary):
        print("-----------New Entry---------------------")

        get_criteria_song(search_criteria)
if sys.argv[1] == "-s":
    #this goes from index 2 all the way to the end
    #slicing is pretty cool huh
    rest = " ".join(sys.argv[2:])
    search_download(rest)

fill_out_library()
