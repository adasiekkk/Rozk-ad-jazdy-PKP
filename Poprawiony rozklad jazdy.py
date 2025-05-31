import pandas as pd

stops = pd.read_csv("C:\\Users\\AdamB\\Downloads\\stops.txt")
stops_time = pd.read_csv("C:\\Users\\AdamB\\Downloads\\stop_times.txt")
transfers = pd.read_csv("C:\\Users\\AdamB\\Downloads\\transfers.txt")
trips = pd.read_csv("C:\\Users\\AdamB\\Downloads\\trips.txt")

poczatek = "Warszawa Centralna"
koniec = "Mława Miasto"
date = "2025-05-22"
hour = "10:00:00"

# Ustawienie typu 'str' dla identyfikatorów stacji
stops["stop_id"] = stops["stop_id"].astype(str)
stops_time["stop_id"] = stops_time["stop_id"].astype(str)

# Konwersja godziny do 'timedelta'
hour = pd.to_timedelta(hour)

# Pobranie identyfikatorów stacji
id_poczatek = str(stops[stops["stop_name"] == poczatek]["stop_id"].iloc[0])
id_koniec = str(stops[stops["stop_name"] == koniec]["stop_id"].iloc[0])

wyniki = []

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

for trip_id in stops_time['trip_id'].unique():
    # Sprawdzamy, czy data się zgadza
    if trip_id[:10] == date:
        trip_data = stops_time[stops_time['trip_id'] == trip_id]
    
        start_row = trip_data[trip_data["stop_id"] == id_poczatek]
        end_row = trip_data[trip_data["stop_id"] == id_koniec]

        if not start_row.empty and not end_row.empty:
            
            if start_row["stop_sequence"].iloc[0] < end_row["stop_sequence"].iloc[0]:
                
                
                departure_time = pd.to_timedelta(start_row["departure_time"].iloc[0])
                
               
                arrival_time_row = stops_time[(stops_time["trip_id"] == trip_id) & (stops_time["stop_id"] == id_koniec)]
                arrival_time = pd.to_timedelta(arrival_time_row["arrival_time"].iloc[0])
                
                kategoria=trips[trips["trip_id"]==trip_id]["route_id"].iloc[0]
                    
                nazwa=trips[trips["trip_id"]==trip_id]["trip_short_name"].iloc[0]
                    
                stacja_koncowa=trips[trips["trip_id"]==trip_id]["trip_headsign"].iloc[0]
                    
                odleglosc_koniec=stops_time[(stops_time["trip_id"]==trip_id) & (stops_time["stop_id"]==id_koniec)]
                odleglosc_koniec=odleglosc_koniec["fare_dist_m"].iloc[0]
                    
                odleglosc_poczatek=stops_time[(stops_time["trip_id"]==trip_id) & (stops_time["stop_id"]==id_poczatek)]
                odleglosc_poczatek=odleglosc_poczatek["fare_dist_m"].iloc[0]
                    
                odleglosc= round((odleglosc_koniec - odleglosc_poczatek)/1000)
                    
                if hour <= departure_time:
                        wyniki.append({
                                        "trip_id":trip_id, 
                                        "kategoria":kategoria, 
                                        "nazwa":nazwa, 
                                        "stacja_koncowa":stacja_koncowa, 
                                        "departure_time":departure_time, 
                                        "arrival_time":arrival_time,
                                        "odleglosc":odleglosc,
                                        "date":date
                                       })
df_wyniki = pd.DataFrame(wyniki)
df_wyniki["departure_time"] = pd.to_timedelta(df_wyniki["departure_time"])
df_wyniki = df_wyniki.sort_values(by="departure_time")
df_wyniki["journey_time"] = df_wyniki["arrival_time"] - df_wyniki["departure_time"]

def format_time_with_day_note(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours >= 24:
        hours -= 24
        return f"{hours:02d}:{minutes:02d} dnia następnego"
    else:
        return f"{hours:02d}:{minutes:02d}"

# Wyświetlanie wyników
for row in df_wyniki.itertuples():
    
    departure_str = str(row.departure_time)
    arrival_str = str(row.arrival_time)
    journey_time_str= str(row.journey_time)
    departure_hours, departure_minutes, departure_seconds = departure_str.split(":")[:3]
    arrival_hours, arrival_minutes, arrival_seconds = arrival_str.split(":")[:3]
    journey_time_hours, journey_time_minutes, journey_time_seconds = journey_time_str.split(":")[:3]
    
    departure_str = format_time_with_day_note(row.departure_time)
    arrival_str = format_time_with_day_note(row.arrival_time)
    journey_time_str = format_timedelta(row.journey_time)

    print(f"Pociąg {row.kategoria} {row.nazwa} do stacji {row.stacja_koncowa}")
    print("Odjazd o godz.:", departure_str)
    print("Przyjazd o godz.:", arrival_str)
    print("Czas przejazdu:.", journey_time_str)
    print()
    
