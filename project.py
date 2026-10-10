import fastf1
import pandas as pd

MIN_YEAR = 2018
MAX_YEAR = 2026

fastf1.Cache.enable_cache('cache')

def main():
    while True:
        text = input("Enter a year: ")
        try:
            race_year = parse_year(text)
            break  
        except ValueError:
            print(f"Please enter a valid year between {MIN_YEAR} and {MAX_YEAR}.")

    schedule = fastf1.get_event_schedule(race_year, include_testing=False)
    max_round = schedule['RoundNumber'].max()
    print("Select a GP:")
    for _, row in schedule.iterrows():
        print(f"{row['RoundNumber']}) {row['EventName']} — {row['Location']}")

    while True:
        round_input = input("Select a round number: ")
        try:
            round_number = parse_round(round_input, max_round)
            break
        except ValueError:
            print(f"Please enter a valid round between 1 and {max_round}.")
    
    session = load_session(race_year, round_number)
    valid_codes = session.results['Abbreviation'].tolist()
    for _, row in session.results.iterrows():
        print(f"{row['Abbreviation']} {row['FullName']} — {row['TeamName']}")

    while True:
        driver_input = input("Select a driver you want to see his results: ")
        try:
            valid_driver = parse_driver(driver_input, valid_codes)
            break
        except ValueError:
            print("Invalid driver")
    driver_results = session.results[session.results['Abbreviation'] == valid_driver]
    
        
    driver_row = driver_results.iloc[0]
    
    position = driver_row['Position']
    grid = driver_row['GridPosition']
    points = driver_row['Points']
    status = driver_row['Status']
    driver_laps = session.laps.pick_drivers(valid_driver)
    
    
    if driver_laps.empty:
        fastest_lap_time = "No laps recorded (DNF)"
    else:
        fastest_lap = driver_laps.pick_fastest()
    
        if pd.isna(fastest_lap['LapTime']):
            fastest_lap_time = "No valid timed lap (NaT)"
        else:

            total_seconds = round(fastest_lap['LapTime'].total_seconds(), 3)
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60
            fastest_lap_time = f"{minutes}:{seconds:06.3f}"
    

    print(f"\n--- Results for {driver_row['FullName']} {driver_row['TeamName']} ({session.event['EventName']} {race_year}) ---")
    print(f"Finishing Position : {int(position)}")
    print(f"Starting Grid      : {int(grid)}")
    print(f"Points Scored      : {points:g}")
    print(f"Status             : {status}")
    print(f"Fastest Lap Time   : {fastest_lap_time}")


def parse_year(text):
    year = int(text)
    if year < MIN_YEAR or year > MAX_YEAR:
        raise ValueError
    return year

def parse_round(text, max_round):
    round_number = int(text)
    if round_number < 1 or round_number > max_round:
        raise ValueError
    return round_number

def parse_driver(text, valid_codes):
    text = text.strip().upper()
    if text not in valid_codes:
        raise ValueError
    return text


def load_session(year, round_number):
    session = fastf1.get_session(year, round_number, 'Race')
    session.load()
    return session


if __name__ == "__main__":
    main()
