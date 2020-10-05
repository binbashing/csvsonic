import hashlib
from urllib2 import urlopen
import ssl
import json
import unicodecsv as csv
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Parse arguements
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server', help='SubSonic URL', required=True)
parser.add_argument('-u', '--username', help='Username', required=True)
parser.add_argument('-p', '--password', help='Password', required=True)
parser.add_argument('-o', '--outfile', help='Output File', required=True)
args = parser.parse_args()

salt = 'qpxzm'
auth_token = args.password + salt
auth_token = hashlib.md5(auth_token)

# Define variables
url_end = "u=%s&t=%s&s=%s&v=1.16.1&c=myapp&f=json" % (args.username, auth_token.hexdigest(), salt)
url_start = "%s/rest/" % (args.server)
output_csv = (args.outfile)

# Handle self signed certificates
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Return a list of dictionaries containing all artists
def get_artists():
    url_action = "getArtists.view?"
    url = url_start + url_action + url_end
    get_results = urlopen(url, context=ctx)
    dict_results = json.load(get_results)
    artist_dict = dict_results['subsonic-response']['artists']['index']
    artist_list = []
    for key in artist_dict:
        for artist in key['artist']:
            artist_list.append(artist)
    return artist_list


# Return a list of dictionaries containing all albums data in the library
def get_albums():
    artist_ids = get_artists()
    album_list = []
    for artist in artist_ids:
        url_action = "getArtist.view?id="
        url = url_start + url_action + artist['id'] + '&' + url_end
        get_results = urlopen(url, context=ctx)
        dict_results = json.load(get_results)
        album_dict = dict_results['subsonic-response']
        for album in album_dict['artist']['album']:
            album_list.append(album)
    return album_list


# Return a list of dictionaries containing all track data in the library
def get_tracks():
    albums = get_albums()
    track_list = []
    for album in albums:
        url_action = "getAlbum.view?id="
        url = url_start + url_action + album['id'] + '&' + url_end
        get_results = urlopen(url, context=ctx)
        dict_results = json.load(get_results)
        track_dict = dict_results['subsonic-response']
        for track in track_dict['album']['song']:
            track_list.append(track)
    return track_list


# Return a list of unique keys for a given list of dictionaries
def get_keys(input_list):
    all_keys = []
    for dictionary in input_list:
        dict_keys = dictionary.keys()
        for key in dict_keys:
            all_keys.append(key)
    all_keys = list(set(all_keys))
    return all_keys


# Generate a csv containing all track data in the library
def all_to_csv():
    track_data = get_tracks()
    print "getting keys"
    keys = get_keys(track_data)
    print "got keys"
    with open(output_csv, 'wb') as output_file:
        print "writing headers"
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(track_data)


all_to_csv()
