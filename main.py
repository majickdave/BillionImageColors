from PIL import Image
import cStringIO
import urllib2

""" 
Need to Implement output .csv --> url;color;color;color 

Must handle large number of input
"""

# COLOR GRABBER - https://gist.github.com/zollinger/1722663 
def getColors(infile, numcolors=3, resize=150):

    image = Image.open(infile)                                              # Using PIL open image
    image = image.resize((resize, resize))                                  # resize image to reduce pixel set
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)   # Convert to image pallete to get dominant colors
    result.putalpha(0)                                                      # Set alpha to zero for RGB
    colors = result.getcolors(resize*resize)                                # get colors in RGB of the resized image
    colors = [y[:-1] for y in [x[-1] for x in colors]]                      # take RGB values
    return colors

# URL READER
def downloadImage(url):
    fl = None
    try:
        fl = cStringIO.StringIO(urllib2.urlopen(url).read())                # create image data from URL string
    except:
        print "Could not Download Image from Url"

    finally:
        # print url, "completed"
        return getColors(fl)                                         # Return the formatted data string

# MAIN APPLICATION
if __name__ == '__main__':
    import numpy as np
    import csv
    import timeit

    # SET URLS
    URLs = set()
    # Processing times
    times = []

    # Read Urls from textfile line by line
    with open("data/urls.txt") as f:

        # CREATE CSV
        csvFile = open("data/output.csv", 'wb')
        for url in f:
            # time each url
            time = timeit.default_timer()
            # check if URL in set
            hmap = url.partition("""//""")[2]       # reduce url string required to search for in set
            if hmap not in URLs:
                print hmap
                # add unique url to set
                URLs.add(hmap)
                # download image from url and get 3 prevalent colors
                data = downloadImage(url)
                # create line writer object for csv file          
                lineWriter = csv.writer(csvFile)
                # write rows per spec
                lineWriter.writerow((url, data[0], data[1], data[2]))
                # track processing time
                times.append((timeit.default_timer() - time))

                print "."*len(url)

        csvFile.close()
        # when no more urls
        print "Mean Processing Time per image: ", round(np.mean(times), 2), "seconds."
        
         









