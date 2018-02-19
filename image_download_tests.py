import unittest
import image_download


class ImageGetterTests(unittest.TestCase):
    def setUp(self):
        # We create an instance with the given source file and specify that test mode is on
        self.images = image_download.ImageGetter(source_file_name='test_links.txt', test_mode=True)

    def test_init(self):
        # The regular expression used to select valid URLs should be a string
        self.assertIsInstance(self.images.matching_string, str)

    def test_construct_raw_list(self):
        # raw_list should be a list instance
        self.assertIsInstance(self.images.raw_list, list)

        # The items of raw_list should be strings
        for item in self.images.raw_list:
            self.assertIsInstance(item, str)

        # The expected raw_list after reading in test_links.txt. The first 2 items are invalid: two URLS in 1 line,
            # and a URL containing unsafe characters
        expected_raw_list = ['http://mywebserver.com/  http://mages/271947.jpg',
                             'http://mywebserver.%^{~/images/271947.com', 'http://somewebsrv.com/img/992147.jpg',
                             'https://www.blue-yonder.com/de',
                             'https://www.blue-yonder.com/sites/default/files/styles/mood_full/public/rgc04_home_page_1.png?itok=MFcd1qVa',
                             'https://media.wired.com/photos/5a7b558800beae0e1d91a5d0/master/w_799,c_limit/03_olympic-village_pyeongchang_31dec2017_wv3.jpg']

        self.assertEqual(self.images.raw_list, expected_raw_list)

    def test_get_one_image(self):

        # Broken/unsafe URL:
        download_feedback0 = self.images.get_one_image('http://mywebserver.%^{~/images/271947.com', 1)
        self.assertEqual(download_feedback0, 'invalidURL')

        # Unreachable URL:
        download_feedback1 = self.images.get_one_image('http://somewebsrv.com/img/992147.jpg', 1)
        self.assertEqual(download_feedback1, 'URLError')

        # Reachable URL but doesn't point to image
        download_feedback2 = self.images.get_one_image('https://www.blue-yonder.com/de', 1)
        self.assertEqual(download_feedback2, 'noImage')

        # Image successfully downloaded
        download_feedback3 = self.images.get_one_image('https://www.blue-yonder.com/sites/default/files/styles/mood_full/public/rgc04_home_page_1.png?itok=MFcd1qVa', 1)
        self.assertEqual(download_feedback3, 'image_1.png')

    # Note: get_images() uses get_one_image() in a loop, so if the latter works fine, the former does too.


if __name__ == '__main__':
    unittest.main()
