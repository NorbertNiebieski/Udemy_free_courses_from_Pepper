import unittest2

import web_bot
import private_date


class MyTestCase(unittest2.TestCase):

    my_bot = None

    @classmethod
    def setUp(self):
        # loading private data
        self.udemy_login = private_date.udemy_login
        self.udemy_password = private_date.udemy_password

        self.pepper_login = private_date.pepper_login
        self.pepper_password = private_date.pepper_password

        self.path_to_chrome_profile = private_date.path_to_chrome_profile

        # depends on your internet connection
        self.sleep_time = 2
        self.printing = True

        # starting bot
        try:
            self.my_bot = web_bot.WebBot(self.udemy_login, self.udemy_password, self.pepper_login, self.pepper_password,
                                         self.path_to_chrome_profile, self.sleep_time, self.printing, "tests.py")
            print("Bot lunch correctly!")
        except Exception as error:
            print(error)
            print("Error when lunching bot")
            exit(-1)

    @classmethod
    def tearDown(self):
        self.my_bot.driver.quit()

    def test_logging_to_udemy(self):
        # self.my_bot.driver.get("https://www.udemy.com/")
        # cookie_access_token = self.my_bot.driver.get_cookie("access_token")
        # cookie_dj_session_id = self.my_bot.driver.get_cookie("dj_session_id")
        # self.my_bot.driver.delete_cookie("access_token")
        # self.my_bot.driver.delete_cookie("dj_session_id")
        try:
            self.assertTrue(self.my_bot.log_to_udemy())
        except Exception as error:
            print(error)
            self.assertTrue(False)
        # finally:
            # self.my_bot.driver.add_cookie(cookie_access_token)
            # self.my_bot.driver.add_cookie(cookie_dj_session_id)
            # print(self.my_bot.driver.get_cookies())


if __name__ == '__main__':
    unittest2.main()
