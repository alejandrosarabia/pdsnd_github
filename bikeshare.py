import time
import pandas as pd
import datetime as dt
import numpy as np
#Change 1
#change 2
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Create dictionaries
months = ['january', 'february', 'march', 'april', 'may', 'june']
month_no = [1,2,3,4,5,6]
dict_months=dict(zip(months,month_no))
days = ['tuesday', 'wednesday','thursday', 'friday', 'saturday','sunday', 'monday']
day_no = [1, 2,3,4,5,6,0]
dict_days=dict(zip(days,day_no))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    while city not in CITY_DATA:
            city = input('Enter the city:').lower()
            if city in CITY_DATA:
                print('This city is on our system')
                break
            else:
                print('Please enter a valid city')

    # get user input for month (all, january, february, ... , june)
    month=''
    while month not in dict_months:
        month = input('Enter the month or all:').lower()
        if (month in dict_months) or (month =='all') :
            print('This month is on our system')
            break
        else:
            print('Please enter a valid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in dict_days:
        day = input('Enter the day or all:').lower()
        if (day in dict_days) or (day == 'all'):
            print('This day is on our system')
            break
        else:
            print('Please enter a valid day')

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
    #Loading the data
    df = pd.read_csv(CITY_DATA[city])
    #Convert date colums to date type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #Create month column
    df['month']=df['Start Time'].dt.month
    #Create day of week column
    df['day_of_week']=df['Start Time'].dt.weekday


    #Filter data frame
    if month!='all':
        month = dict_months[month]
        is_month = df['month']==month
        df = df[is_month]

    if day!= 'all':
        day=dict_days[day]
        is_day = df['day_of_week']==day
        df = df[is_day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print(df.head())
    start_time = time.time()

    # TO DO: display the most common month
    most_month = df['month'].mode()[0]
    most_month = [k for k, v in dict_months.items() if v == most_month][0]
    print('the most common month was ' + most_month)

    # TO DO: display the most common day of week
    most_day = df['day_of_week'].mode()[0]
    print(most_day)
    most_day = [k for k, v in dict_days.items() if v == most_day][0]
    print('the most common day was ' + most_day)

    # TO DO: display the most common start hour
    most_hour = str(df['Start Time'].dt.hour.mode()[0])
    print('the most common hour was ' + most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start=str(df['Start Station'].value_counts().idxmax())

    print('The most popular Start station was ' + most_start)

    # TO DO: display most commonly used end station
    most_end=str(df['End Station'].value_counts().idxmax())

    print('The most popular End station was ' + most_end)

    # TO DO: display most frequent combination of start station and end station trip

    most_stations= df.groupby(['Start Station','End Station'])['End Station'].count().idxmax()

    print('The most common statiosn are ' + str(' and '.join(most_stations)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Duration']= df['End Time']- df['Start Time']
    print('Total travel time ' + str(df['Duration'].sum()))


    # TO DO: display mean travel time
    print('Mean travel time ' + str(df['Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if 'User Type' in df:

    # TO DO: Display counts of user types
        print(df['User Type'].value_counts())
    else: print('User Type stats cannot be calculated because User Type does not appear in the dataframe')

    # TO DO: Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else: print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        df = df[df['Birth Year'].notna()]
        df_recent = df.sort_values(by='End Time', ascending=False).head(1).iloc[0]['Birth Year']
        print('The most recent customer was born in ' + str(df_recent))
        print('The oldest customer was born in ' + str(df['Birth Year'].min()))
        print('The younguest customer was born in ' + str(df['Birth Year'].max()))
        print('The common is ' + str(df['Birth Year'].mode()[0]))
    else:print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

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
        raw_data= input('\nWould you like to see the raw data (5 lines)? Enter yes or no.\n')

        #Show raw data
        x=5
        while True:
            if raw_data.lower() == 'yes':

                print(x)
                print (df.head(x))
                raw_data= input('\nWould you like to see the 5 more lines of data? Enter yes or no.\n')
                if raw_data == 'yes':
                    x = x + 5
                    print(x)
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
