import time
import pandas as pd
import click

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
MONTHS = ('january', 'february', 'march', 'april', 'may', 'june')
WEEKDAYS = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

def get_valid_choice(prompt, choices=('y', 'n')):
    """Prompt the user until a valid choice is made."""
    while True:
        choice = input(prompt).lower().strip()
        if choice == 'end':
            raise SystemExit
        elif ',' not in choice:
            if choice in choices:
                return choice
        else:
            selected_choices = [i.strip().lower() for i in choice.split(',')]
            if all(c in choices for c in selected_choices):
                return selected_choices
        
        prompt = "\nInvalid input. Please enter a valid option:\n>"

def get_filters():
    """Ask user for city, month, and day filters."""
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Type 'end' at any time to exit the program.\n")

    while True:
        city = get_valid_choice("\nSelect a city (New York City, Chicago, Washington):\n>", CITY_DATA.keys())
        month = get_valid_choice("\nSelect a month (January to June):\n>", MONTHS)
        day = get_valid_choice("\nSelect a weekday:\n>", WEEKDAYS)

        confirmation = get_valid_choice(f"\nConfirm filters:\n City: {city}\n Month: {month}\n Weekday: {day}\n [y] Yes\n [n] No\n>", ('y', 'n'))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try again!")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """Load data for specified city, filtering by month and day."""
    print("\nLoading data for your selected filters...")
    start_time = time.time()

    if isinstance(city, list):
        df = pd.concat((pd.read_csv(CITY_DATA[c]) for c in city), sort=True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if isinstance(month, list):
        df = pd.concat([df[df['Month'] == (MONTHS.index(m) + 1)] for m in month])
    else:
        df = df[df['Month'] == (MONTHS.index(month) + 1)]

    if isinstance(day, list):
        df = pd.concat([df[df['Weekday'] == d.title()] for d in day])
    else:
        df = df[df['Weekday'] == day.title()]

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)
    return df

def display_time_stats(df):
    """Display statistics on the most frequent travel times."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['Month'].mode()[0]
    most_common_day = df['Weekday'].mode()[0]
    most_common_hour = df['Start Hour'].mode()[0]

    print(f'Most common month: {MONTHS[most_common_month - 1].title()}')
    print(f'Most common day: {most_common_day}')
    print(f'Most common start hour: {most_common_hour}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_station_stats(df):
    """Display statistics on the most popular stations and trips."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    
    df['Start-End'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_start_end = df['Start-End'].mode()[0]

    print(f'Most common start station: {most_common_start_station}')
    print(f'Most common end station: {most_common_end_station}')
    print(f'Most common trip: {most_common_start_end}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_trip_duration_stats(df):
    """Display statistics on total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    total_duration_str = f"{total_travel_time // 86400}d {total_travel_time % 86400 // 3600}h {total_travel_time % 3600 // 60}m {total_travel_time % 60}s"
    mean_duration_str = f"{mean_travel_time // 60}m {mean_travel_time % 60}s"

    print(f'Total travel time: {total_duration_str}')
    print(f'Mean travel time: {mean_duration_str}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts().to_string()
    print("User types distribution:\n" + user_types)

    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nGender distribution:\n" + gender_distribution)
    except KeyError:
        print(f"No gender data available for {city.title()}.")

    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print(f"\nOldest user birth year: {earliest_birth_year}")
        print(f"Youngest user birth year: {most_recent_birth_year}")
        print(f"Most common birth year: {most_common_birth_year}")
    except KeyError:
        print(f"No birth year data available for {city.title()}.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Display raw data in chunks."""
    print("\nYou opted to view raw data.")
    start_index = 0

    while True:
        if start_index >= len(df):
            print("No more data to display.")
            break

        print(df.iloc[start_index:start_index + 5].to_string())
        start_index += 5

        if get_valid_choice("Do you want to see more raw data? [y/n]\n>") != 'y':
            break

def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while True:
            selected_stat = get_valid_choice("\nSelect the information you would like:\n [ts] Time Stats\n [ss] Station Stats\n [tds] Trip Duration Stats\n [us] User Stats\n [rd] Raw data\n [r] Restart\n>", ('ts', 'ss', 'tds', 'us','rd', 'r'))
            click.clear()

            if selected_stat == 'ts':
                display_time_stats(df)
            elif selected_stat == 'ss':
                display_station_stats(df)
            elif selected_stat == 'tds':
                display_trip_duration_stats(df)
            elif selected_stat == 'us':
                display_user_stats(df, city)
            elif selected_stat == 'rd':
                mark_place = display_raw_data(df)
            elif selected_stat == 'r':
                break

        if get_valid_choice("\nWould you like to restart? [y/n]\n>") != 'y':
            break

if __name__ == "__main__":
    main()