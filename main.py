import pepper_free_course
import private_date
from time import sleep

def main_test():

    pepper_login = private_date.pepper_login
    pepper_password = private_date.pepper_password

    # depends of your internet connection
    sleep_time = 2

    try:
        my_bot = pepper_free_course.PepperBot()
    except:
        print("Something went wrong with lunch pepper bot")
        return -1
    else:
        print("Pepper bot lunch correctly!")

    my_bot.log_to_pepper_account(pepper_login, pepper_password)
    #promotion_links = my_bot.find_udemy_promotions_on_pepper()
    my_bot.give_plus_pepper_promotion("https://www.pepper.pl/promocje/maslo-200-g-82-przy-zakupie-3-szt-at-carrefour-421593")
    sleep(5)

    my_bot.driver.close()


def main():

    # in the another python file you could do your on file with this string or write your login and password below
    udemy_login = private_date.udemy_login
    udemy_password = private_date.udemy_password

    # in the another python file you could do your on file with this string or write your login and password below
    pepper_login = private_date.pepper_login
    pepper_password = private_date.pepper_password

    # Write pepper promotion url below
    # url = ""

    # url = input("Pepper's promotion url: ")

    # depends of your internet connection
    sleep_time = 2
    printing = True

    try:
        my_bot = pepper_free_course.PepperBot()
    except:
        print("Something went wrong with lunch pepper bot")
        return -1
    else:
        print("Pepper bot lunch correctly!")

    my_bot.log_to_pepper_account(pepper_login, pepper_password)

    promotion_links = my_bot.find_udemy_promotions_on_pepper()

    # taking links from pepper
    # try:
    #     links = my_bot.taking_links_to_udemy_from_pepper_promotion(url)
    # except:
    #     print("I can't find any links to udemy!")
    #     return -1

    links = []

    for promotion_link in promotion_links:

        links += my_bot.taking_links_to_udemy_from_pepper_promotion(promotion_link)
        try:
            my_bot.give_plus_pepper_promotion()
        except:
            print("There was an error adding the plus!")

    if not links:
        return 0

    # logging to udemy
    # try:
    #     check_log_in = my_bot.log_to_udemy(udemy_login, udemy_password, printing, sleep_time)
    # except Exception as e:
    #     print("I can't log to your udemy account!")
    #     print(e)
    #     check_log_in = False
    #     return -1
    # finally:
    #     if check_log_in == False:
    #         return -1

    # checking every link
    saving = 0
    course_number = 0
    number_of_course = len(links)
    for link in links:
        course_number += 1
        try:
            saving += my_bot.buy_free_course(link, sleep_time, course_number, number_of_course)
        except:
            print("Something went wrong with this link: " + link)

    # printing stats and ending
    my_bot.printing_stats_udemy_courses()
    print("You are save: " + str(round(saving, 2)))
    my_bot.driver.close()

main()