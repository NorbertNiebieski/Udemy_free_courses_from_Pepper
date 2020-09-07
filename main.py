import pepper_free_course
import private_date

if __name__ == '__main__':

    my_bot = pepper_free_course.PepperBot()

    # in the another python file you could do your on file with this string or write your login and password below
    udemy_login = private_date.udemy_login
    udemy_password = private_date.udemy_password

    # Write pepper promotion url below
    url = ""

    # depends of your internet connection
    sleep_time = 10

    # taking links from pepper
    links = my_bot.talking_links_to_udemy_from_pepper_promotion(url)

    # logging to udemy
    my_bot.log_to_udemy(udemy_login, udemy_password)

    # checking every link
    for link in links:
        my_bot.buy_free_course(link, sleep_time)

    # printing stats and ending
    my_bot.printing_stats_udemy_courses()
    my_bot.driver.close()