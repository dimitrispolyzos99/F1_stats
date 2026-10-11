import fastf1
import pandas as pd
import matplotlib.pyplot as plt

MIN_YEAR = 2018
MAX_YEAR = 2026

def main():
    fastf1.Cache.enable_cache('cache')
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
        has_telemetry = False
    else:
        fastest_lap = driver_laps.pick_fastest()
    
        if pd.isna(fastest_lap['LapTime']):
            fastest_lap_time = "No valid timed lap (NaT)"
            has_telemetry = False
        else:
            fastest_lap_time = format_lap_time(fastest_lap['LapTime'].total_seconds())
            has_telemetry = True
    
    try:
        gained = positions_gained(int(grid), int(position))
        gained_text = f"{gained:+}"
    except ValueError:
        gained_text = "Pit lane start"

    lines = [
        f"Finishing Position : {int(position)}",
        f"Starting Grid      : {int(grid)}",
        f"Points Scored      : {points:g}",
        f"Status             : {status}",
        f"Fastest Lap Time   : {fastest_lap_time}",
        f"Positions Gained   : {gained_text}"]
    result_title = (f"Results for {driver_row['FullName']}\n{driver_row['TeamName']}\n({session.event['EventName']} {race_year})")
    info = "\n".join(lines)
    board = f"{result_title}\n\n{info}"
    print(board)
    
    if has_telemetry:
        title = (f"Fastest Lap Telemetry — {session.event['EventName']}\n({driver_row['FullName']} - {driver_row['TeamName']}) {fastest_lap_time}")
        telemetry = fastest_lap.get_telemetry()
        plot_track(telemetry, title, board)
    else:
        print("No telemetry available to plot.")


def format_lap_time(seconds):
    seconds = round(seconds, 3)
    minutes = int(seconds // 60)
    format_seconds = seconds % 60
    return f"{minutes}:{format_seconds:06.3f}"

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

def plot_track(telemetry, title, info):
    plt.figure(figsize=(13, 6))
    plt.scatter(telemetry['X'], telemetry['Y'], c=telemetry['Speed'], s=5, cmap='plasma')
    plt.axis('equal')
    plt.axis('off')
    plt.colorbar(label='Speed (km/h)')
    plt.title(title)
    plt.subplots_adjust(right=0.7)
    plt.figtext(
        0.75, 0.5, info, 
        family='monospace', 
        va='center', 
        bbox=dict(
            boxstyle='round,pad=0.5', 
            facecolor='whitesmoke', 
            edgecolor='lightgray', 
            linewidth=1.2
        )
    )
    
    plt.show() 

def positions_gained(grid, finish):
    if grid == 0:
        raise ValueError("Grid position 0 is not valid for calculating positions gained (pit lane start).")
    return grid - finish


if __name__ == "__main__":
    main()
