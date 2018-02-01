# download_amos.py
# Austin Abrams, 2/16/10
# a helper utility to download and unzip a lot of images from the AMOS dataset.

import os
import sys
import urllib2
import StringIO
import zipfile
import threading
import time
# Change this to where you want data to be dumped off.  If not supplied, defaults to
# the current working directory.
# example:
# ROOT_LOCATION = '/path/to/where/you/want/AMOS_Data/'
ROOT_LOCATION = '/home/old-ufo/dev/amos_download/data/'
URLS_LIST_FNAME = 'current_amos_urls.txt'
# change these parameters as necessary to download whichever camera or year or month you
# want to download.
#CAMERAS_TO_DOWNLOAD = [90]
#YEARS_TO_DOWNLOAD = [2013]
#MONTHS_TO_DOWNLOAD = range(1,13)
#MONTHS_TO_DOWNLOAD = [9]
# if the script crashed or the power went out or something, this flag will
# skip downloading and unzipping a month's worth of images if there's already
# a folder where it should be.  If you set this to false, then downloads
# will overwrite any existing files in case of filename conflict.
SKIP_ALREADY_DOWNLOADED = True

# maximum number of threads allowed. This can be changed.
MAX_THREADS = 100

class DownloadThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url =url
        t = url.split('/')
        self.camera_id = t[-2]
        self.year = t[-1].split('.')[0]
        self.month = t[-1].split('.')[1]
    def run(self):
        location = ROOT_LOCATION + self.camera_id +'/' + self.year + '.' + self.month  + '/'
        if SKIP_ALREADY_DOWNLOADED and os.path.exists(location):
            print(location + " already downloaded.")
            return
        print("downloading to " + location)
        zf = download(self.url)
        print("completed downloading to " + location)
        if not zf:
            print("skipping " + location)
            return
        ensure_directory_exists(location)
        print("Extracting from " + location)
        extract(zf, location)
        print("Done")
        return
def download(url):
    """
    Downloads a zip file from AMOS, returns a file.
    """
    try:
        result = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print e.code, 'error.'
        return None
    handle = StringIO.StringIO(result.read())
    #print 'done.'
    sys.stdout.flush()
    return handle
    
def extract(file_obj, location):
    """
    Extracts a bunch of images from a zip file.
    """
    #print '    extracting zip...',
    sys.stdout.flush()
    zf = zipfile.ZipFile(file_obj, 'r')
    zf.extractall(location)
    zf.close()
    file_obj.close()
    #print 'done.'
    sys.stdout.flush()
    return 
def ensure_directory_exists(path):
    """
    Makes a directory, if it doesn't already exist.
    """
    dir_path = path.rstrip('/')       
    if not os.path.exists(dir_path):
        parent_dir_path = os.path.dirname(dir_path)
        ensure_directory_exists(parent_dir_path)
        try:
            os.makedirs(dir_path)
        except OSError:
            pass
    return 
def main():
    # for all cameras...
    with open(URLS_LIST_FNAME, 'rb') as f:
        urls = f.readlines()
    for url in urls:
        url = url.strip()
        thread_count = threading.activeCount()
        while thread_count > MAX_THREADS:
                print("Waiting for threads to finish...")
                time.sleep(1)
                thread_count = threading.activeCount()              
        download_thread = DownloadThread(url)
        download_thread.start()
    return 
if __name__ == '__main__':
    if ROOT_LOCATION == None:
        ROOT_LOCATION = os.getcwd() + '/AMOS_Data'
    if ROOT_LOCATION[-1] != '/':
        ROOT_LOCATION = ROOT_LOCATION + '/'
    print 'Downloading images to:'
    main()
