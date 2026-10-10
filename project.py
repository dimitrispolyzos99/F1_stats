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
    print("Select a GP:")
    for race_round, row in schedule.iterrows():
        print(f"{row['RoundNumber']}) {row['EventName']} — {row['Location']}")
    round_input = input("Select a round number: ")
    
    session = load_session(race_year, round_number=int(round_input))
    
    driver_abbr = 'VER'
    driver_results = session.results[session.results['Abbreviation'] == driver_abbr]
    
    if driver_results.empty:
        print(f"Driver {driver_abbr} not found in this session.")
        return
        
    driver_row = driver_results.iloc[0]
    
    position = driver_row['Position']
    grid = driver_row['GridPosition']
    points = driver_row['Points']
    status = driver_row['Status']
    driver_laps = session.laps.pick_drivers(driver_abbr)
    
    
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
    

    print(f"\n--- Results for {driver_abbr} ({session.event['EventName']} {race_year}) ---")
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


def load_session(year, round_number):
    session = fastf1.get_session(year, round_number, 'Race')
    session.load()
    return session


if __name__ == "__main__":
    main()
