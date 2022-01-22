from datetime import datetime
import time
from tkinter import E
from tokenize import group
from turtle import clear
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITY_ASCII = {'c': '''
                                                                         
           88          88                                                
           88          ""                                                
           88                                                            
 ,adPPYba, 88,dPPYba,  88  ,adPPYba, ,adPPYYba,  ,adPPYb,d8  ,adPPYba,   
a8"     "" 88P'    "8a 88 a8"     "" ""     `Y8 a8"    `Y88 a8"     "8a  
8b         88       88 88 8b         ,adPPPPP88 8b       88 8b       d8  
"8a,   ,aa 88       88 88 "8a,   ,aa 88,    ,88 "8a,   ,d88 "8a,   ,a8"  
 `"Ybbd8"' 88       88 88  `"Ybbd8"' `"8bbdP"Y8  `"YbbdP"Y8  `"YbbdP"'   
                                                 aa,    ,88              
                                                  "Y8bbdP"       
            ''',
              'n': '''
                                     | |   
 _ __   _____      ___   _  ___  _ __| | __
| '_ \ / _ \ \ /\ / / | | |/ _ \| '__| |/ /
| | | |  __/\ V  V /| |_| | (_) | |  |   < 
|_| |_|\___| \_/\_/  \__, |\___/|_|  |_|\_\\
                      __/ |                
                     |___/  
                     ''',
              'w': '''                                                           
                              888     d8b                888                    
                             888     Y8P                888                    
                             888                        888                    
888  888  888 8888b. .d8888b 88888b. 88888888b.  .d88b. 888888 .d88b. 88888b.  
888  888  888    "88b88K     888 "88b888888 "88bd88P"88b888   d88""88b888 "88b 
888  888  888.d888888"Y8888b.888  888888888  888888  888888   888  888888  888 
Y88b 888 d88P888  888     X88888  888888888  888Y88b 888Y88b. Y88..88P888  888 
 "Y8888888P" "Y888888 88888P'888  888888888  888 "Y88888 "Y888 "Y88P" 888  888 
                                                     888                       
                                                Y8b d88P                       
                                                 "Y88P" 
              '''}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*'*40)
    print('*'*40)
    print("""
        o__      __o        ,__o        __o           __o
    ,>/_       -\<,      _-\_<,       _`\<,_       _ \<_
    (*)`(*).....O/ O.....(*)/'(*).....(*)/ (*).....(_)/(_)
    """)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('*'*40)
    print('*'*40)
    # DONE: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = {'c':'Chicago', 'n':'New York City', 'w':'Washington'}
    c = None
    options = ['c', 'n', 'w', 'q']
    while not c or c[0].lower() not in options :
        c = input(
            '\nPlease select what city to analyzes: (c) Chicago, (n) New York or (w) Washington (q) to Quit\n ')
        try:
            c = c[0].lower()
        except:
            c = ' '
        if not c or c not in options:
            print(f'!!!!{c}!!!!! is not a valid option please try again')
        if c == 'q':
            print('I see a "q"\nGoodbye!')
            exit()
    city = cities[c]
    c_ascii = CITY_ASCII[c]
    print(f'Ok we are analyzing {city}!!!')
    print(f'{c_ascii}')

    #lets ask the user if hw wants to filter by month or day
    filter = input("Would you like to add filter:\n Type (y) for Yes or just hit Enter to start analyzing:\n")
    if filter.lower() != 'y':
        print('Here we go!\n')
        print('*'*40)
        print('<','-'*38,'> \n')
        return city, 'all', 'all'
    else:
    # DONE: get user input for month (all,)
        months = ['all','January', 'February', 'March', 'April', 'May', 'June']
        m = input(
            '\n Select the month number (1-6) to analiza or just hit enter to analizas all\n')
        try:
            month = months[int(m)]
        except: 
            month = 'all'
        print(f'\nYou selected {city.title()} and {month.title()}')

        # DONE: get user input for day of week (all, monday, ... sunday)
        day_or_week = {'a':'all', 'm':'Monday', 't':'Tuesday', 'w':'Wednesday', 'r':'Thursday', 'f':'Friday', 's':'Saturday', 'u':'Sunday'}
        
        d = input(
            '\n Select the day of the week (m) Monday, (t) Tuesday, (w) Wednesday, (r) Thursday, (f) Friday, (s) Saturday, (u) Sunday or just hit enter to analizas all\n')
        try:
            day = day_or_week[d[0].lower()]
        except: 
            day = 'all'

        print(f'\nYou selected {city}, {month} and {day}')

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
    df['city'] = city
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start month'] = df['Start Time'].dt.month_name()
    df['Start hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        df = df[df['Start month'] == month]

    # # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    # join Start Stop Station to df
    df['Start Stop Station'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')

    # print('we are returning the dataframe\n')
    # print(df[['city','Start Time','Start month','Start hour', 'day_of_week', 'Start Stop Station']])
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # DONE: display the most common month
    common_month = df['Start month'].mode()[0]
    print(f'The most common month is {common_month}')
    # DONE: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"\nThe most common day of the week is {common_day}")

    # DONE: display the most common start hour
    common_start_hour = df['Start hour'].mode()[0]
    print(f"\nThe most common start hour is : {common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # DONE: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"\nThe most common start station is : {common_start_station}")

    # DONE: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most common end station is : {common_end_station}")

    # DONE: display most frequent combination of start station and end station trip
    common_start_end_station = df['Start Stop Station'].mode()[0]
    print(f"\nThe most common start and end station is : {common_start_end_station}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # DONE: display total travel time
    print(f'\nThe total travel time is {df["Trip Duration"].sum()} seconds')

    # DONE: display mean travel time
    print(f'\nThe mean travel time is {df["Trip Duration"].mean()} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # DONE: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'\nThe counts of user types are :\n{user_types}')

    # DONE: Display counts of gender
    gender_types = df['Gender'].value_counts()
    print(f'\nThe counts for gender type are :\n{gender_types}')
 

    # TO DO: Display earliest, most recent, and most common year of birth
    common_year = df['Birth Year'].mode()[0]
    #group_birth = df.groupby(['city']).agg('minBD'=np.min,'maxBD'=np.max))
    #group_birth.agg(minYear=('Birth Year', np.min), maxYear=('Birth Year', np.max))
   # print(f'\ngroup birth: {group_birth.head()}')
    #print(  f'The earliest year of birth is {df2.minYear.min()} \nthe most recent year of birth is {df2.maxYear.max()} \nAnd the most common year of birth is {common_year}')

    #print(f'The earliest year of birth is {group_birth['amin']} \nthe most recent year of birth is {group_birth.['amax']} \nAnd the most common year of birth is {common_year}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    """
    Displays raw data for user to see

    Args: df - Pandas DataFrame containing city data filtered by month and day

    returns: Console output of raw data
    """
    view_data = input(
        '\nWould you like to view 5 rows of individual trip data? Enter (y) Yes or (n) No\n')


    start_loc = 0
    while  view_data and (view_data.lower()[0] == 'y'):
        print(df[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?(y) or just hit Enter to stop   \n").lower()
    
    print('-'*40)
    




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print( df.columns)
        # time_stats(df)
        # time.sleep(1)
        # station_stats(df)
        # time.sleep(1)
        #trip_duration_stats(df)
        if city.lower() != 'washington':
            time.sleep(1)
            user_stats(df)
        view_data(df)
       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
