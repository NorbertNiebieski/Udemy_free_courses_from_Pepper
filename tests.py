import unittest
from time import sleep

import web_bot
import private_date


class MyTestCase(unittest.TestCase):
    def test_something(self):
        pepper_login = private_date.pepper_login
        pepper_password = private_date.pepper_password

        # depends on your internet connection
        sleep_time = 2

        try:
            my_bot = web_bot.WebBot()
        except:
            print("Something went wrong with lunch pepper bot")
            return -1
        else:
            print("Pepper bot lunch correctly!")

        my_bot.log_to_pepper_account(pepper_login, pepper_password)
        # promotion_links = my_bot.find_udemy_promotions_on_pepper()
        my_bot.give_plus_pepper_promotion(
            "https://www.pepper.pl/promocje/maslo-200-g-82-przy-zakupie-3-szt-at-carrefour-421593")
        sleep(5)

        my_bot.driver.close()


if __name__ == '__main__':
    unittest.main()
