import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
       
    while True:
        try:
            city = input("Please tell me what city (Chicago, Washington or New York City) you want to see data for:").lower()
            if city == 'chicago' or city == 'washington' or city == 'new york city':
                break
            else:
                print("Invalid input, try again. Make sure to choose a valid city.")
        except:
            print("Invalid input, try again.")
    print("Great, we'll check {}!".format(city.title()))   


    '''Asks user if they want to filter by month, day or not at all. Depending on the answer, checks for specific filter requirements.'''
    while True:
        filter = input("Do you want to filter by month, day or neither: ").lower()
        if filter == "month":
            # get user input for month (all, january, february, ... , june)
            while True:
                try:
                    month = input("Please tell me what month (January through June) you want to see data for. If you want the whole year, write 'all': ").lower()
                    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
                    day =  "all"
                    if month in valid_months:
                        break
                    elif month == 'all':
                        break
                    else:
                        print("Invalid input, try again. Make sure to choose a valid month.")
                except:
                    print("Invalid input, try again.")
            print("Great, we'll check {}!".format(month.title()))
            break
        elif filter == "day":
            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                try:
                    day = input("Please tell me what day of the week you want to see data for. If you want the whole week, write 'all': ").lower()
                    valid_days = list(calendar.day_name)
                    month = "all"
                    if day.title() in valid_days:
                        break
                    elif day == 'all':
                        break
                    else:
                        print("Invalid input, try again. Make sure to choose a valid day.")
                except:
                    print("Invalid input, try again.")
            print("Great, we'll check {}!".format(day.title()))
            break
        elif filter == "neither":
            print("neither")
            month = "all"
            day =  "all"
            break
        else:
            print("Invalid input, try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]
    print('Most common day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

        # display most commonly used start station
    print("Most common Start Station:", df["Start Station"].mode().values)


        # display most commonly used end station
    print("Most common End Station:", df["End Station"].mode().values)


# display most frequent combination of start station and end station trip
    Start_End = [df["Start Station"],df["End Station"]]
    print("The most common Start Station and End Station combination and the amount of travels taken is as follows:",
          pd.MultiIndex.from_arrays(Start_End).value_counts().head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_traveltime = df["Trip Duration"].sum()
    print("Overall travel time in min:", total_traveltime/60)


    # display mean travel time
    mean_traveltime = df["Trip Duration"].mean()
    print("Mean travel time in min:", mean_traveltime/60)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

        # Display counts of user types
    print("User Type counts are as follows:", df.groupby(["User Type"])["User Type"].count())

        # Display counts of gender. As not all cities provide this data, a check is implemented.
    try:
        print("Gender counts are as follows:", df.groupby(["Gender"])["Gender"].count())
    except:
        print("No Gender data avialable.")

        # Display earliest, most recent, and most common year of birth. As not all cities provide this data, a check is implemented.
    try:
        print("Earliest birth year:", int(df["Birth Year"].min()))
        print("Most recent birth year:", int(df["Birth Year"].max()))
        print("Most common birth year:", int(df["Birth Year"].mode()))
    except:
        print("No Birth Year data available.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Checking if the user wants to see 5 rows of data, giving 5 rows until no more are requested.
        start = 0
        end = 5
        first_five_rows = input('\nWould you like to see 5 rows of data? Enter yes or no.\n')
        if first_five_rows.lower() == 'yes':
            while True:
                try:
                    print(df[start:end])
                    
                    five_rows = input('\nWould you like 5 more rows? Enter yes or no.\n')
                    if five_rows.lower() != 'yes':
                        break
                    else:
                        start += 5
                        end += 5
                except:
                    print("An error occurred, no rows can be shown.")
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
