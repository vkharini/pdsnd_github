#Load libraries
import datetime as dt
import time
import pandas as pd
import numpy as np

#Include data files to be used and time period for filter in lists
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec","all"]
day_list=["mon","tue","wed","thu","fri","sat","sun","all"]

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
    city=input("\nWhich city do you want to explore, chicago, new york city or washington : ").lower()
    while city not in CITY_DATA:
        print("\nOops, looks like there is some error with the entry. Let us try again..")
        city=input("\nWhich city do you want to explore, chicago, new york city or washington : ").lower()

    # get user input for month (all, january, february, ... , june)
    month=input("\nWhich month do you want to explore the data for? \nType any one of jan-dec. or all if you want for all months : ").lower()
    while month not in month_list:
        print("\nOops, looks like there is some error with the entry. Let us try again..")
        month=input("\nWhich month do you want to explore the data for? \nType any one of jan-dec. or all if you want for all months : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input("\nWhich day of the week do you want to explore the data for? \nType any one of mon-sun. or all if you want for all days: ").lower()
    while day not in day_list:
        print("\nOops, looks like there is some error with the entry. Let us try again..")
        day=input("\nWhich day of the week do you want to explore the data for? \nType any one of Mon-Sun. or all if you want for all days: ").lower()

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
    df=pd.read_csv(CITY_DATA[city])

    df["Start Time"]=pd.to_datetime(df["Start Time"])
    df["month_num"]=df["Start Time"].dt.month
    df["weekday_num"]=df["Start Time"].dt.weekday
    df["hour"]=df["Start Time"].dt.hour
    for i in df.index:
        temp_m=month_list[df["month_num"][i]-1]
        df.at[i,"month"]=temp_m

        temp_d=day_list[df["weekday_num"][i]]
        df.at[i,"weekday"]=temp_d

    df["city"]=city

    if month!="all":
        df=df[df["month"]==month]

    if day!="all":
        df=df[df["weekday"]==day]
    
    print("\nThe filtered data set contains {} rows of data".format(df["city"].count()))
    
    
    #Reconfirming the filtering criteria with the user
    
    while True:
        check=input("\nWould you like to proceed with this or provide a different filtering criteria?\nType yes to proceed and no to provide different filtering criteria :")
        if check.lower()=="yes":
            break
        elif check.lower()=="no":
            main()
        else:
            print("\nPlease type only yes or no")
    
    print("-"*40)
    return df

     
def view_raw_data(df):
    count=0
    ans=input("Do you wish to see first 5 rows of the filtered data set? Type yes or no : ")
    if ans.lower()=="yes":
        print(df.iloc[0:5])
        while True:
            answer=input("Do you wish to see 5 more rows of the filtered data set? Type yes or no : ")
            if answer.lower()=="yes":
                count+=5
                print(df.iloc[count:count+5])
            elif answer.lower()=="no":
                print("\nAlright!Proceeding to the next step.")
                print("-"*40)
                break
            else:
                print("\nPlease type only yes or no\n")
    elif ans.lower()=="no":
        print("\nAlright!Proceeding to the next step.")
        print("-"*40)
    else:
        print("\nPlease type only yes or no\n")
        view_raw_data(df)




def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel.....\n')
    start_time = time.time()

    # display the most common month
    if month!="all":
        print("You asked for data related to only ",month)
    else:
        c_month=df["month"].mode()[0]
        print("Most common month for this data set is :",c_month)


    # display the most common day of week
    if day!="all":
        print("You asked for data related to only ",day)
    else:
        c_day=df["weekday"].mode()[0]
        print("Most common day of week for this data set is :",c_day)

    # display the most common start hour
    c_hour=df["hour"].mode()[0]
    print("Most common start hour for this data set is :",c_hour)

    print("\nThe above calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    c_s_st=df["Start Station"].mode()[0]
    print("Most commonly used start station is : ",c_s_st)

    # display most commonly used end station
    c_e_st=df["End Station"].mode()[0]
    print("Most commonly used end station is : ",c_e_st)

    # display most frequent combination of start station and end station trip
    df["combo"]=df["Start Station"]+" to "+df["End Station"]
    c_combo=df["combo"].mode()[0]
    print("Most frequently used combination for start and end station trip is :",c_combo)

    print("\nThe above calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time for this data set is :",df["Trip Duration"].sum())

    # display mean travel time
    print("Average travel time for this data set is :",df["Trip Duration"].mean())

    print("\nThe above calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Below are the user types for this data set :\n",df["User Type"].value_counts())

    # Display counts of gender
    if df["city"].iloc[0] in ["chicago","new york city"]:
        print("Below are the gender counts for this data set :\n",df["Gender"].value_counts())
    else:
        print("No gender data available for this data set")

    # Display earliest, most recent, and most common year of birth


    if df["city"].iloc[0] in ["chicago","new york city"]:
        e_yob=int(df["Birth Year"].min())
        print("The earliest year of birth in the data set is :",e_yob)
        r_yob=int(df["Birth Year"].max())
        print("The most recent year of birth in the data set is :",r_yob)
        c_yob=int(df["Birth Year"].mode()[0])
        print("The most common year of birth in the data set is :",c_yob)
    else:
        print("No Birth Year available for this data set")


    print("\nThe above calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        view_raw_data(df)
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
