"""
This script for the 506 Waiver. Here are my information:
Name: Licheng Zhu
UMID: 58432543
Email: zlicheng@umich.edu
"""


# import statements
import unittest
import json
import requests
import pickle
import logging
#import ast

# logging.basicConfig(level=logging.INFO)

###### INTRODUCTION #########

# Complete this problem set to assess for yourself and demonstrate to us that you are ready to place out of UMSI106 (for BSI students) or UMSI506 (for MSI/MHI students).
#
# If you're not yet an expert in python, or just need a refresher, you will probably find it useful to consult the online textbook that has been used for teaching UMSI106 and will also be used for UMSI506. You can find it at https://www.programsinformationpeople.org/runestone/static/publicPIP/

# For setting up your python programming environment, you may want to consult the installation chappter, starting at: https://www.programsinformationpeople.org/runestone/static/publicPIP/Installation/FirstSteps.html

# This assignment requires some knowledge of all the chapters in the text *except* those titled, "Prediction and Classification", "Inheritance", "Pyglet", "The Facebook Graph API", "Recursion",  "Test Cases", and "Unix". Some hints are provided with specific problems about chapters you might want to consult.

#
# There is code at the bottom of the file that runs tests: once you complete your part of the code, as instructed, all those tests should pass. Don't change any of the tests! You don't even need to understand the python unit test framework in which they are written. You can just examine in the outputs that they generate in your terminal (command prompt) window.


###### END OF INTRODUCTION #######


# [PROBLEM 1]
# REF: chapter on Classes, starting at https://www.programsinformationpeople.org/runestone/static/publicPIP/Classes/intro-ClassesandObjectstheBasics.html

# Here is a class definition to represent a photo object. Take a look at the code and make sure you understand it.

class Photo():
    def __init__(self, title, author, tags):
        self.title = title
        self.author = author
        self.tags = tags
    def __str__(self):
        return "({}, {}, {})".format(self.title, self.author, self.tags)

my_photo = Photo("Photo1", "Ansel Adams", ['Nature', 'Mist', 'Mountain'])
#print my_photo

## Write one line of code to create an instance of the photo class and store the instance in a variable my_photo.
## After you do that, my_photo.title should have the value "Photo1", my_photo.author should have the value "Ansel Adams" and my_photo.tags should have the value ['Nature', 'Mist', 'Mountain']).

# HINT: if you just call the constructor for the Photo class appropriately, everything will be taken care of for you. You just have to figure out, from the definition of the class, what to pass to the constructor. Remember the examples of creating a class instance from the textbook!


# [PROBLEM 2]
# REF: chapters on Dictionaries, Files, and for converting the text into a dictionary, the discussion of json.loads() in https://www.programsinformationpeople.org/runestone/static/publicPIP/RESTAPIs/jsonlib.html

# REF: https://www.programsinformationpeople.org/runestone/static/publicPIP/NestedData/DebuggingNestedData.html

# Now suppose that we revise the Photo class. Instead of passing into the constructor three separate values, the revised constructor will take a dictionary of data and extract those three values. The structure of the dictionary will be determined by the way the flickr API returns data.

# We have provided a sample dictionary in the format that Flickr returns it. Let's read it in from a file. Feel free to add some print statements to understand the structure of sample_d. You may also find it useful to open the file "sample_d.txt" in a text editor, or copy and paste its contents into http://www.jsoneditoronline.org/

f = open("sample_d.txt", "r")
sample_d = json.loads(f.read())
f.close()

# Your job is to fill in the __init__ method
class Photo2():
    def __init__(self, photo_d):
        self.title = (photo_d['photo']['title']['_content']).encode('utf-8')
        self.author = (photo_d['photo']['owner']['username']).encode('utf-8')
        self.tags = [(x['raw']).encode('utf-8') for x in photo_d['photo']['tags']['tag']]
    def __repr__(self):   #using the special __repr__ method for later 
        return "({}, {}, {})".format(self.title, self.author, self.tags)

#print Photo2(sample_d)

# After you fill it in, try creating an instance by invoking Photo2(sample_d) and check to see if it has the values you expect for title, author, and tags.


### PART 2: FlickR Tag Recommender



flickr_key = '88c582e55511629d1c00f987981f5a6f' # paste your flickr key here, so the variable flickr_key contains a string (your flickr key!)
if not flickr_key:
    flickr_key = raw_input("Enter your flickr API key, or paste it in the .py file to avoid this prompt in the future: \n>>")

## Useful function definitions provided for you below.

#### Now we'll walk you through steps you need to take to make a tag recommender, but we won't be providing you any code. You'll use the documentation we've copied in here and the functions provided above to translate the English into Python and make your program work.

# You will go through these steps using cached data stored in the file we have provided, "cached_results.txt". This will insulate you from potential problems with network connections while you are debugging your data processing code. It also makes it easier for us to grade the problem set, because everyone's program will work with the same code. If you'd like to run it with live data, simply change the value of the variable cache_fname to some other file name, and you will be working with a fresh, empty cache.

# REF: You'll need to read the chapters titled: Python Modules, Requests, REST APIs, and Using RESTAPIs

# REF: The code below is explained in https://www.programsinformationpeople.org/runestone/static/publicPIP/UsingRESTAPIs/cachingResponses.html

cache_fname = "cache.bin"
try:
    fobj = open(cache_fname, 'rb')
    saved_cache = pickle.load(fobj)
    fobj.close()
except:
    raise Exception("Make sure you have cached_results.txt in the same directory as this code file.")
    # saved_cache = {}

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = params)
    prepped = req.prepare()
    return prepped.url

def get_with_caching(base_url, params_diction, cache_diction, cache_fname, omitted_keys = ['api_key']):
    filtered_params_diction = {}
    for k in params_diction:
        if k not in omitted_keys:
            filtered_params_diction[k] = params_diction[k]
    full_url = requestURL(base_url, filtered_params_diction)
    # step 1
    if full_url in cache_diction:
        # step 2
        logging.info("retrieving cached result for " + full_url)
        return cache_diction[full_url]
    else:
        # step 3
        response = requests.get(base_url, params=params_diction)
        logging.info("adding cached result for " + full_url)
        # add to the cache and save it permanently
        cache_diction[full_url] = response.text
        fobj = open(cache_fname, "wb")
        pickle.dump(cache_diction, fobj)
        fobj.close()
        return response.text

# [PROBLEM 3]

# Get a response from flickr: data for 50 photos that are tagged with 'sunset'. Store the list of dictionaries in a variable called search_result_txt. See the textbook section on the flickr API, and see the documentation page at https://www.flickr.com/services/api/flickr.photos.search.html

params_d = {}
params_d['method'] = 'flickr.photos.search'
params_d['api_key'] = flickr_key
params_d['format'] = 'json'
params_d['tags'] = 'sunset'
params_d['per_page'] = 50
search_result_txt = get_with_caching('https://api.flickr.com/services/rest/', params_diction= params_d, 
                                     cache_diction = saved_cache, cache_fname = cache_fname)
#print type(search_result_txt)
#print search_result_txt

# [PROBLEM 4] Extract and parse as json

# search_result contains a long string, with the annoying extra characters that the flickr api adds at the beginning and end of its response text. Strip off the extra characters and turn the remaining json-formatted text string into a python dictionary. (Hint: see the flickr section of the UsingRESTAPIs chapter for a  reminder of how to do this.) Save the dictionary in a variable called search_result_diction

#this is my solution solving the "unicode" issue without involking json.loads.
import ast    #converted parsed search_result_txt to a dict
search_result_diction = ast.literal_eval(search_result_txt[14:-1])

#print search_result_diction
#print type(d)


# [PROBLEM 5] Extract a list of photo ids from the dictionary. Use a list comprehension or a call to map in order to do this.

# REF: Read the chapter titled: "More on Accumulation: Map, Filter, Reduce, List Comprehensions, and Zip"

photo_ids_list = [x['id'].encode('utf-8') for x in search_result_diction['photos']['photo']]
#print photo_ids_list[0]
#print photo_ids_list, type(photo_ids_list), type(photo_ids_list[0])


# [PROBLEM 6] Get info from flickr about each photo id

## Create an instance of Photo2 for each of the photo ids.

#a) make a request to the flickr API method flickr.photos.getInfo instead of flickr.photos.search. See documentation at https://www.flickr.com/services/api/flickr.photos.getInfo.html for what to pass as extra parameters.
#b) Extract a dictionary from the response for each.
#c) Pass the dictionary when constructing a new instance of Photo2
#d) Accumulate the instance into a list, called photo_instances

def get_id_info(id):
    params_d_id = {}
    params_d_id['method'] = 'flickr.photos.getInfo'
    params_d_id['api_key'] = flickr_key
    params_d_id['format'] = 'json'
    params_d_id['photo_id'] = id
    search_result_diction_id = json.loads(get_with_caching('https://api.flickr.com/services/rest/', params_diction= params_d_id, 
                                     cache_diction = saved_cache, cache_fname = cache_fname)[14:-1])
    #search_result_diction_id ={str(key):value for key,value in search_result_diction_id.items()}  
    #above is my failed attempt to convert the dictionary to the one with unicode values
    instance = Photo2(search_result_diction_id)
    return instance
photo_instances = [get_id_info(x) for x in photo_ids_list]

# [PROBLEM 7] Accumulate frequencies of related tags.
# You started out with data about 50 different photos, including the tags that the photo owners used to describe the photos. They all have the tag 'sunset', since that's the tag we searched for, but some have additional tags, like 'river' and 'nature' and others. Accumulate a dictionary of counts; call the dictionary counts_diction.

# REF: See the chapter titled, "Accumulating Results in Dictionaries"

# getting all tags into a list
counts_list = [x.tags for x in photo_instances]

def get_elements(counts_list):  #flatten out the nested list 'counts_list'
    counts_list_tag = []
    for i in counts_list:
        if type(i) == list:
            counts_list_tag.extend(get_elements(i))
        else:
            counts_list_tag.append(i)
    return counts_list_tag

my_list = get_elements(counts_list)

# counting the tags
counts_diction = {} 
for i in my_list:
    if i not in counts_diction:
        counts_diction[i] = 1
    else:
        counts_diction[i] += 1

#print counts_diction


# [PROBLEM 8] Sort the tags

# Sort all the tags in descending order based on how often they were used in the 50 photos. Save the sorted list in a variable called sorted_tags.

# REF: See the chapter titled, "Sorting"

sorted_tags = sorted(counts_diction.keys(), key=lambda x: counts_diction[x], reverse=True)

#print type(sorted_tags)
#print sorted_tags


# [PROBLEM 9] Output five recommended tags


## Print, for the user to see, the five tags (other than the searched on tag, sunset) that were used MOST frequently!

## HINT 1: Take a slice of the sorted list.
## HINT 2: Skip the first element in the sorted list. That will be "sunset", since all the photos have that tag.

# REF: Slicing is in one of the early chapters, titled, "Sequences"

print "Below this line, the 5 most frequently used tags should print out:"

n = 0 #counter
recommended_list = sorted_tags[1:6]
for i in recommended_list:
    n += 1
    print "{}. {}".format(n, i)

print "-----------------done; output of diagnostic tests is below this line------------"





##### Code for running diagnostic tests are below this line. Don't change any code below this line######
class Problem1(unittest.TestCase):
    def test_title(self):
        self.assertEqual(my_photo.title, "Photo1")
    def test_author(self):
        self.assertEqual(my_photo.author, "Ansel Adams")
    def test_tags(self):
        self.assertEqual(my_photo.tags, ['Nature', 'Mist', 'Mountain'])

class Problem2(unittest.TestCase):
    def setUp(self):
        f = open("sample_d.txt", "r")
        sample_d = json.loads(f.read())
        f.close()
        self.p2 = Photo2(sample_d)

    def test_title(self):
        self.assertEqual(self.p2.title, "Photo1")
    def test_author(self):
        self.assertEqual(self.p2.author, "Ansel Adams")
    def test_tags(self):
        self.assertEqual(self.p2.tags, ['Nature', 'Mist', 'Mountain'])

class Problem3(unittest.TestCase):
    def test_prefix(self):
        self.assertEqual(search_result_txt[:14], "jsonFlickrApi(", "Check starting characters")

class Problem4(unittest.TestCase):
    def test_01(self):
        self.assertIn('photos',search_result_diction, "Check if 'photos' is a key" )
    def test_02(self):
        self.assertIn('photo',search_result_diction['photos'], "Check for search_result_diction['photos']['photo']")
    def test_03_check_length(self):
        self.assertEqual(len(search_result_diction['photos']['photo']), 50, "check if 50 photos returned")

class Problem5(unittest.TestCase):

    def test_01(self):
        self.assertEqual(len(photo_ids_list), 50, "Check id count")

    def test_02(self):
        self.assertEqual(photo_ids_list[0], "27733361503", "Check first id")

class Problem6(unittest.TestCase):

    def test_01(self):
        self.assertEqual(len(photo_instances), 50, "Check count")

    def test_02(self):
        self.assertEqual(photo_instances[0].tags, ['Sunset', 'Bavaria'], "Check tags of first instance")

class Problem7(unittest.TestCase):

    def test_01(self):
        self.assertEqual(counts_diction['water'], 3, "water count")
        self.assertEqual(counts_diction['snow'], 1, "Outdoors count")

class Problem8(unittest.TestCase):

    def test_01(self):
        self.assertEqual(sorted_tags[:10], [u'sunset', u'Lake Geneva', u'Andrew Wilson Switzerland', u'Lausanne', u'Switzerland', u'Sunset', u'Clouds', u'landscape', u'Sun', u'sUNSET'], "Check sorted tags")


unittest.main(verbosity=2)

