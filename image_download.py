import re
import urllib.request
import logging


class ImageGetter:
    """Class to download images belonging to URLs, contained in an input plain text source file.
    The source file is supposed to contain a single URL per line.

    Attributes:
        raw_list (list) -- Its items contain the individual lines from the original text file.
        matching_string (str) -- Regular expression string used to match links that contain characters for a valid URL.
        filtered_list (list) -- Contains the items from raw_list that are valid URLs.
    """

    raw_list = []
    matching_string = ''
    filtered_list = []

    def __init__(self, **kwargs):
        """Initialises raw_list, matching string, and generates a logging instance.

        Keyword arguments:
             'source_file_name' -- Name of the plain text file containing the source text.
             'test_mode' -- If set to True, it means we want to test the class: no logging instance is created.
                Default: 'False'
             'log_file_name' -- Name of the log file. If given 'test mode' Default name: image_getter.log
             'log_level' -- The logging threshold, by default put to logging.DEBUG

        """

        self.construct_raw_list(kwargs.get('source_file_name'))
        self.matching_string = r"^(http|https)://[\w\-.$+!'*,;/?:@=&]+$"
        self.test_mode = kwargs.get('test_mode', False)

        if not self.test_mode:
            log_file_name = kwargs.get('log_file_name', 'image_getter.log')
            log_level = kwargs.get('log_level', logging.DEBUG)

            logging.basicConfig(filename=log_file_name, level=log_level)

    def construct_raw_list(self, file_name):
        """Method to construct raw_list. It parses the source plain text file into a string, then assigns each line as
         a separate item to raw_list. It also strips the items from potential whitespaces around them.

        Arguments:
            file_name -- Name of the source file containing a single URL per line.
        """

        source_file = open(file_name, encoding='UTF-8')
        source = source_file.read()
        source_file.close()
        self.raw_list = list(map(lambda item: item.strip('\s'), source.split('\n')))

    def filter_links(self):
        """Method for choosing the valid URLs from raw_list. It uses matching_string to decide,
        and puts the valid links into filtered_list. It also logs the presence of invalid links into the log file.
        """

        for line in range(0, len(self.raw_list)):
            match = re.match(self.matching_string, self.raw_list[line])
            if match:
                self.filtered_list.append(match.group())
            elif not self.test_mode:
                logging.warning("Line {} in source file broken or not a valid URL format.".format(line + 1))

        if not self.test_mode:
            logging.info("------------- Links filtered -------------\n")

    def get_one_image(self, link, image_index):
        """Method for downloading an image belonging to a single URL.
        It checks if the URL is reachable. If not reachable, it returns 'URLError'.
        Else, it checks whether the content of the URL is an image. If it's an image, it downloads it, and returns
        the file name under which it has been saved on the hard disk.
        if it isn't an image, then it returns 'noimage'.

        Arguments:
            link (str) -- the URL we want to download.
            image_index (str) -- the running index to construct the file name upon saving: 'image_<image_index>.ext'
        """

        try:
            content = urllib.request.urlopen(link)
        except urllib.request.URLError:
            return 'URLError'
        else:
            content_type = content.info().get_content_type()
            if 'image' in content_type:
                image_extension = re.search(r"(\w+)$", content_type).group()

                image = urllib.request.urlretrieve(link, 'image_' + str(image_index) + '.' + image_extension)

                return image[0]
            else:
                return "noimage"

    def get_images(self):
        """Method for looping through filtered_list and downloading the images its items point to, using download_link().
        For each item, it checks the returned value of download_link(), and logs it into the log file if the download
        was unsuccessful.
        """

        image_index = 0
        for link in self.filtered_list:

            download_feedback = self.get_one_image(link, image_index)

            if download_feedback == 'URLError' and not self.test_mode:
                logging.warning("{} - URL error.".format(link))
            elif download_feedback == 'noimage' and not self.test_mode:
                logging.warning(link + " does not point to an image.")
            else:
                image_index += 1

        if not self.test_mode:
            logging.info("------------- Images downloaded -------------\n")


if __name__ == '__main__':

    # Example: create an instance of ImageGetter, reading in 'links.txt' as source file
    images = ImageGetter(source_file_name='test_links.txt')

    # Filter links that are broken or invalid
    images.filter_links()
    # Download images, using the valid URLs
    images.get_images()