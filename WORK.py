from urllib.request import urlopen, Request
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import random
from io import BytesIO

class Trip:
    def __init__(self, city, date, price, description):
        self.city = city
        self.date = date
        self.price = price
        self.description = description

    def __eq__(self, other):
        return self.city == other.city and self.date == other.date

    def __hash__(self):
        return hash((self.city, self.date))

planned_trips = set()


city_images = {
    "Paryż": "https://a.eu.mktgcdn.com/f/100004519/N2BB4ohwclor2uLoZ7XMHgJmxOZaMOokMdQqqXQAq3s.jpg",
    "Rzym": "https://cdn.britannica.com/16/99616-050-72CD201A/Colosseum-Rome.jpg",
    "Berlin": "https://ocdn.eu/pulscms-transforms/1/_Ilk9kpTURBXy8wNTc0ZDJhOWNhNTg0MTVmNmNmYTRlYmRjMGU2NzI0NC5qcGeTlQMBzGrNA-fNAjGTCaZjYzU1NTAGkwXNBLDNAnbeAAGhMAE/berlin-miasto-po-drodze-fot-shutterstock.jpg",
    "Londyn": "https://babylontours.com/wp-content/uploads/2016/09/london-441853_960_720.jpg",
    "Madryd": "https://www.civitatis.com/f/pseo/espana/madrid/gran-via-noche-madrid-1200.jpg",
    "Praga": "https://www.agoda.com/wp-content/uploads/2024/04/Featured-image-Scenic-Prague-panorama-with-Hradcany-castle-and-Vltava-river-in-spring-Czech-Republic-1244x700.jpg",
    "Wiedeń": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/11/6b/48/6d/photo0jpg.jpg?w=900&h=500&s=1",
    "Amsterdam": "https://static01.nyt.com/images/2023/09/24/multimedia/24-36Hrs-Amsterdam-01-01-cwqt/24-36Hrs-Amsterdam-01-01-cwqt-superJumbo.jpg",
    "Barcelona": "https://sitgesluxuryrentals.com/wp-content/uploads/2017/05/barcelona1.jpg"
}

city_description = {
    "Paryż": "Miasto miłości i światła, słynne z wieży Eiffla, Luwru i romantycznej atmosfery na brzegach Sekwany.",
    "Rzym": "Wieczne miasto pełne zabytków, takich jak Koloseum, Forum Romanum czy Watykan. Historia na każdym kroku.",
    "Berlin": "Stolica Niemiec, gdzie nowoczesność spotyka się z burzliwą historią. Znany z Bramy Brandenburskiej i Muru Berlińskiego.",
    "Londyn": "Kosmopolityczna metropolia z ikonami, takimi jak Big Ben, Tower Bridge i Pałac Buckingham. Stolica kultury i biznesu.",
    "Madryd": "Energetyczne miasto pełne sztuki (Prado), flamenco i hiszpańskiej kuchni. Królewska elegancja połączona z życiem nocnym.",
    "Praga": "Perła Europy Środkowej z malowniczym Starym Miastem, Zamkiem Praskim i słynnym Mostem Karola nad Wełtawą.",
    "Wiedeń": "Stolica muzyki i cesarskiego splendoru, gdzie można podziwiać pałace, takie jak Schönbrunn i Hofburg, oraz delektować się tortem Sachera.",
    "Amsterdam": "Miasto kanałów, rowerów i artystycznego ducha. Znane z muzeum Van Gogha, domu Anny Frank i kwitnących tulipanów.",
    "Barcelona": "Połączenie architektury Gaudiego, plaż i śródziemnomorskiej kuchni. Tętniąca życiem stolica Katalonii."
}

def generate_random_trips():
    cities = ["Paryż", "Rzym", "Berlin", "Londyn", "Madryd", "Praga", "Wiedeń", "Amsterdam", "Barcelona"]
    trips = []
    for city in cities:
        price = random.randint(10, 100) * 10
        date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%d.%m.%Y")
        description = city_description.get(city)
        trips.append(Trip(city, date, price, description))
    return trips

def show_planned_trips():
    planned_window = tk.Toplevel()
    planned_window.title("My Planned Trips")
    planned_window.geometry("800x600")

    if not planned_trips:
        tk.Label(planned_window, text="No trips planned yet.", font=("Helvetica", 14)).pack(pady=20)
        return

    for idx, trip in enumerate(planned_trips):
        frame = tk.Frame(planned_window, relief="solid", borderwidth=1)
        frame.pack(pady=5, padx=10, fill="x")

        tk.Label(frame, text=f"{idx + 1}. {trip.city} - {trip.date}", font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Label(frame, text=f"Price: ${trip.price}", font=("Helvetica", 10)).pack(anchor="w")
        tk.Label(frame, text=f"Description: {trip.description}", font=("Helvetica", 10), wraplength=400, justify="left").pack(anchor="w")

        tk.Button(frame, text="Cancel Trip", command=lambda t=trip, f=frame: cancel_trip(t, f), bg="red", fg="white").pack(anchor="e")

def cancel_trip(trip, frame):
    planned_trips.remove(trip)
    frame.destroy()
    messagebox.showinfo("Cancelled", f"Trip to {trip.city} has been cancelled.")

def show_trip_details(trip):
    def reserve_trip():
        if trip in planned_trips:
            messagebox.showwarning("Warning", f"The trip to {trip.city} on {trip.date} is already planned!")
        else:
            planned_trips.add(trip)
            messagebox.showinfo("Reservation", f"You have successfully reserved a trip to {trip.city} on {trip.date}!")
        details_window.destroy()

    details_window = tk.Toplevel()
    details_window.title("Trip Details")
    details_window.geometry("400x300")

    tk.Label(details_window, text=f"Destination: {trip.city}", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(details_window, text=f"Date: {trip.date}", font=("Helvetica", 12)).pack()
    tk.Label(details_window, text=f"Price: ${trip.price}", font=("Helvetica", 12)).pack()
    tk.Label(details_window, text="Description:", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Label(details_window, text=trip.description, wraplength=300, justify="center").pack(pady=10)

    tk.Button(details_window, text="Reserve Trip", command=reserve_trip, bg="green", fg="white").pack(pady=20)

def create_app():
    trips = generate_random_trips()
    root = tk.Tk()
    root.title("Travel Reservation App")
    root.geometry("800x600")

    tk.Label(root, text="Travel Reservation", font=("Helvetica", 20, "bold")).pack(pady=10)

    tk.Button(root, text="My Planned Trips", command=show_planned_trips, bg="blue", fg="white").pack(pady=5)

    trips_frame = tk.Frame(root)
    trips_frame.pack()

    for i, trip in enumerate(trips):
        frame = tk.Frame(trips_frame, relief="solid", borderwidth=1)
        frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)

        photo = get_city_image(trip.city)

        if photo:
            photo_label = tk.Label(frame, image=photo)
            photo_label.image = photo  
            photo_label.pack()

        tk.Label(frame, text=trip.city, font=("Helvetica", 14, "bold")).pack()
        tk.Label(frame, text=f"Price: ${trip.price}", font=("Helvetica", 10)).pack()
        tk.Label(frame, text=f"Date: {trip.date}", font=("Helvetica", 10)).pack()

        tk.Button(frame, text="View Details", command=lambda t=trip: show_trip_details(t)).pack(pady=5)

    root.mainloop()

def get_city_image(city):
    url = city_images.get(city)
    if not url:
        return None

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            img_data = response.read()
        img = Image.open(BytesIO(img_data))
        img = img.resize((150, 100))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image for {city}: {e}")
        return None

create_app()
