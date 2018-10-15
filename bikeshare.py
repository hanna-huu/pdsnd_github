import time
import pandas as pd
import numpy as np

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
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("\nWould you like to see data for Chicago, New York City, or Washington?")

    while city.lower() != 'chicago' and city.lower() != 'new york city' and city.lower() != 'washington':
        city = input("\nPlease enter a valid city: Would you like to see data for Chicago, New York City, or Washington?")

    # get user input for month (all, january, february, ... , june)

    month = input("\nWhich month you would like to filter data - January, February, March, April, May, or June? Type all if you want no filter.").lower()

    while month.lower() != 'january' and month.lower() != 'february' and month.lower() != 'march' and month.lower() != 'april' and month.lower() != 'may' and month.lower() != 'june' and month.lower() != 'all':
        month = input("\nPlease enter a valid month: January, February, March, April, May, or June? Type all if you want no filter.")

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type all if you want no filter.").lower()

    while day.lower() != 'monday' and day.lower() != 'tuesday' and day.lower() != 'wednesday' and day.lower() != 'thursday' and day.lower() != 'friday' and day.lower() != 'saturday' and day.lower() != 'sunday' and day.lower() != 'all':
        day = input("\nPlease enter a valid day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type all if you want no filter.")


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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


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

    # display the most common month


    popular_month = df['month'].mode()[0]

    print('Most Frequent month: {}'.format(popular_month))

    # display the most common day of week

    popular_day = df['day_of_week'].mode()[0]

    print('Most Frequent day: {}'.format(popular_day))
    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    print('Most Frequent hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular Start Station:', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('Most popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start_and_end_station'] = df['Start Station'] + ' TO ' + df['End Station']
    popular_start_and_end_station = df['start_and_end_station'].mode()[0]
    print('Most frequent combination of start station and end station trip:', popular_start_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time

    total_trip_duration_mean = df['Trip Duration'].mean()
    print('Mean trip duration time:', total_trip_duration_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()

    print('Subscribers:', user_types[0])
    print('Customers:', user_types[1])

    if city.lower() != 'washington':
        # Display counts of gender

        gender_count = df['Gender'].value_counts()
        print("\n")
        print('Males:', gender_count[0])
        print('Females:', gender_count[1])

        # Display earliest, most recent, and most common year of birth

        print("\n")
        print('Earliest year of birth is', int(df['Birth Year'].min()))
        print('Most recent year of birth is', int(df['Birth Year'].max()))
        print('Most common year of birth is', int(df['Birth Year'].mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    else:
        print('\nGender and Birth Year information is not available')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # ask user if he/she wants to see raw data

        raw_data = ''
        while raw_data != 'no':
            raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')

            if raw_data.lower() == 'yes':
                number_of_rows = input('\nHow many rows of data would you like to see. Enter an integer.\n')
                print(df.head(int(number_of_rows)))

            else:
                print('\nPlease give a valid answer.')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
