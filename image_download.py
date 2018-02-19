import re
import urllib.request
import logging


class ImageGetter:
    """Class to download images belonging to URLs, contained in an input plain text source file.
    The source file is supposed to contain a single URL per line.

    Attributes:
        raw_list (list) -- Its items contain the individual lines from the original text file.
        matching_string (str) -- Regular expression string used to match links that contain characters for a valid URL.
        test_mode (boolean) -- If True, it indicates that test mode is active and logging is suppressed. Otherwise, a
            logging instance is created to contain information about URL validity and the success of image downloads.
    """

    raw_list = []
    matching_string = ''
    test_mode = False

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

    def get_one_image(self, link, image_index):
        """Method for downloading an image belonging to a single URL.
        It checks if the URL is in a valid format and if it contains unsafe characters. If the string value does not
        fit that of a valid URL, it raises a ValueError.

        If the URL format is all right, it checks if the URL is reachable. If not reachable, it raises a
        urllib.request.URLError.

        If the content type of the URL is not an image, a TypeError is raised.

        Otherwise, it downloads the image at the URL location.

        Arguments:
            link (str) -- the URL we want to download.
            image_index (str) -- the running index to construct the file name upon saving: 'image_<image_index>.ext'
        """
        match = re.match(self.matching_string, link)

        if not match:
            raise ValueError  # The URL string does not match the expected value

        content = urllib.request.urlopen(link)
        content_type = content.info().get_content_type()

        if 'image' not in content_type:
            raise TypeError  # The type of the content the URL points to is not an image

        else:
            image_extension = re.search(r"(\w+)$", content_type).group()
            image = urllib.request.urlretrieve(link, 'image_' + str(image_index) + '.' + image_extension)

            return image[0]

    def get_images(self):
        """Method for looping through raw_list and downloading the images its items point to, using get_one_image().
        For each item, it tries to call get_one_image(), and (depending on the exception raised) logs it into the
         log file if there was a problem with the URL (pointing out the line in the original source file), if the URL
          was unreachable, or if the content type of the URL was not an image.
        """

        image_index = 0
        line_index = 0
        for link in self.raw_list:

            try:
                self.get_one_image(link, image_index)
            except ValueError:
                logging.warning("Line {} in source file broken or not a valid URL format.".format(line_index + 1))
            except urllib.request.URLError:
                logging.warning("{} - URL error.".format(link))
            except TypeError:
                logging.warning(link + " does not point to an image.")
            else:
                image_index += 1

            line_index += 1

        logging.info("------------- Images downloaded -------------\n")


if __name__ == '__main__':

    # Example: create an instance of ImageGetter, reading in 'links.txt' as source file
    images = ImageGetter(source_file_name='test_links.txt')

    # Download images, using the valid URLs
    images.get_images()
