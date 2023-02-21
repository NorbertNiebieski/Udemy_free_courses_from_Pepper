import web_bot
import private_data
import log


def main():
    # in the another python file you can write your login and password to udemy account
    try:
        udemy_login = private_data.udemy_login
        udemy_password = private_data.udemy_password
        log.root.info("Loading udemy account credential from private_data.py")
    except Exception as error:
        log.root.info("Getting udemy account credential from user input, because %s", error, exc_info=1)
        print("You can create file private_data.py and write there your login an password to udemy account")
        udemy_login = input("Please, write your udemy account login")
        udemy_password = input("Please, write your udemy account password")

    # in the another python file you can write your login and password to pepper account
    try:
        pepper_login = private_data.pepper_login
        pepper_password = private_data.pepper_password
        log.root.info("Loading pepper account credential from private_data.py")
    except Exception as error:
        log.root.info("Getting pepper account credential from user input, because %s", error, exc_info=1)
        print("You can create file private_data.py and write there your login an password to pepper account")
        pepper_login = input("Please, write your pepper account login")
        pepper_password = input("Please, write your pepper account password")

    # in the another python file you can write path to your chrome profile
    try:
        path_to_chrome_profile = private_data.path_to_chrome_profile
        log.root.info("Loading path to chrome profile from private_data.py")
    except Exception as error:
        log.root.info("Getting path to chrome profile from user input, because %s", error, exc_info=1)
        print("You can create file private_data.py and write there path to your chrome profile")
        path_to_chrome_profile = input("Please, write path to your chrome profile or leave blank")

    # depends on your internet connection
    sleep_time = 2

    # starting bot
    try:
        my_bot = web_bot.WebBot(udemy_login, udemy_password, pepper_login, pepper_password, path_to_chrome_profile,
                                sleep_time)
        log.log_and_print("info", "Bot lunch correctly!")
    except Exception as error:
        log.log_and_print("error", "Something went wrong with lunch bot", error)
        return -1

    # logging to pepper account
    try:
        my_bot.log_to_pepper_account()
    except Exception as error:
        log.log_and_print("warning", "I was unable to log your pepper account", error)

    # finding promotions with udemy courses
    try:
        promotion_links = my_bot.find_udemy_promotions_on_pepper()
    except Exception as error:
        log.log_and_print("error", "There was error with finding udemy promotions", error)
        return -1

    links = []

    # extracting links to udemy courses and adding plus to pepper promotion
    for promotion_link in promotion_links:
        try:
            links += my_bot.taking_links_to_udemy_from_pepper_promotion(promotion_link)
        except Exception as error:
            log.log_and_print("warning", "There was problem with extracting links from this pepper promotion - " +
                              str(promotion_link), error)
        try:
            my_bot.give_plus_pepper_promotion()
        except Exception as error:
            log.log_and_print("warning", "There was problem with adding the plus this pepper promotion - " +
                              str(promotion_link), error)

    if not links:
        return 0

    # logging to udemy account
    try:
        if not my_bot.log_to_udemy():
            return -1
    except Exception as error:
        log.log_and_print("error", "There was problem with logging to your udemy account", error)
        return -1

    # checking every link
    saving = 0
    course_number = 0
    number_of_course = len(links)
    for link in links:
        course_number += 1
        try:
            saving += my_bot.buy_free_course(link, course_number, number_of_course)
        except Exception as error:
            log.log_and_print("warning", "Something went wrong with this link - " + link, error)

    # printing stats and ending
    try:
        if log.is_printing:
            my_bot.printing_stats_udemy_courses()
    except Exception as error:
        log.log_and_print("warning", "Something went wrong when printing stats", error)

    if log.is_printing:
        print("You saved: " + str(round(saving, 2)))
    my_bot.driver.quit()


if __name__ == '__main__':
    main()
