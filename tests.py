import unittest2

import web_bot
import private_data

import log


class MyTestCase(unittest2.TestCase):
    printing = True
    sleep_time = 5
    path_to_chrome_profile = ""
    pepper_password = ""
    pepper_login = ""
    udemy_password = ""
    udemy_login = ""
    __my_bot = None

    @classmethod
    def setUp(cls):
        # loading private data
        cls.udemy_login = private_data.udemy_login
        cls.udemy_password = private_data.udemy_password

        cls.pepper_login = private_data.pepper_login
        cls.pepper_password = private_data.pepper_password

        cls.path_to_chrome_profile = private_data.path_to_chrome_profile

        # depends on your internet connection
        cls.sleep_time = 2
        cls.printing = True

        # variable to storing cookies
        cls.__stored_cookies = {}

        # starting bot
        try:
            cls.__my_bot = web_bot.WebBot(cls.udemy_login, cls.udemy_password, cls.pepper_login,
                                          cls.pepper_password,
                                          cls.path_to_chrome_profile, cls.sleep_time, cls.printing, "tests.py")
            print("Bot lunch correctly!")
            log.root.info("Bot lunch correctly!")
        except Exception as error:
            print("Something went wrong with lunch bot")
            log.root.error("Something went wrong with lunch bot - %s", error, exc_info=1)
            return -1

    @classmethod
    def tearDown(cls):
        cls.__my_bot.driver.quit()

    def test_logging_to_pepper(self):
        self.__storing_and_deleting_cookies("https://www.pepper.pl/", ["remember_6fc0f483e7f442dc50848060ae780d66",
                                                                       "pepper_session"])
        try:
            self.assertTrue(self.__my_bot.log_to_pepper_account())
        except Exception as error:
            log.root.error("Error when logging to pepper account - %s", error, exc_info=1)
            self.__adding_stored_cookies("https://www.pepper.pl/")
            self.assertTrue(False, "Error when logging to pepper account")

    def test_logging_to_udemy(self):
        self.__storing_and_deleting_cookies("https://www.udemy.com/", ["access_token", "dj_session_id"])
        try:
            self.assertTrue(self.__my_bot.log_to_udemy())
        except Exception as error:
            log.root.error("Error when logging to udemy account - %s", error, exc_info=1)
            self.__adding_stored_cookies("https://www.udemy.com/")
            self.assertTrue(False, "Error when logging to udemy account")

    def __adding_stored_cookies(self, cookies_domain):
        if self.__my_bot.driver.current_url != cookies_domain:
            self.__my_bot.driver.get(cookies_domain)
        for cookie in self.__stored_cookies.pop(cookies_domain):
            self.__my_bot.driver.add_cookie(cookie)

    def __storing_and_deleting_cookies(self, cookies_domain, cookies_names):
        if self.__my_bot.driver.current_url != cookies_domain:
            self.__my_bot.driver.get(cookies_domain)
        cookies_to_store = []
        for cookie in cookies_names:
            cookies_to_store.append(self.__my_bot.driver.get_cookie(cookie))
            self.__my_bot.driver.delete_cookie(cookie)
        self.__stored_cookies[cookies_domain] = cookies_to_store


if __name__ == '__main__':
    unittest2.main()
