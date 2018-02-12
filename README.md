# Image-downloader
Python (3.x) script for downloading images from URLs contained in a source text file.
Also, an example source file is added, containing valid and broken links.
It also contains a unit test script, testing the methods and functionalities of the original code.
Upon execution (except in test mode), a log file is created where information about the invalid URLs, as well as about failed attempts to download an image is collected.

Instructions:
  - create an ImageGetter() instance specifying the source text file
  - call the .filter_links() method to filter out the invalid links from the original ensemble
  - call the .get_images() method to download the images the URLs point to
  - You're done! :)
