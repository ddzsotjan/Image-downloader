# Image-downloader
Python (3.x) script (**image_download.py**) for downloading images from URLs contained in a source text file. Upon execution (except in test mode), a log file is created where information about the invalid URLs, as well as about failed image downloads are collected.
Also, an example source file (**test_links.txt**) is added, containing valid and broken links.
A unit test script (**image_download_tests.py**) tests the methods and functionalities of the original code.

Instructions for using **image_download.py**:
  - create an ImageGetter() instance specifying the source text file
  - call the .get_images() method to download the images the URLs point at
  - You're done! :)
