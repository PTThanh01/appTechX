from PIL import Image, ImageTk
import networkx as nx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkComboBox, CTkLabel, CTkButton


# Create window customtkinter
root = ctk.CTk()
root.title("Find Hotel")
root.geometry("600x600")



destinations = ["Sân bay","Bệnh viện Chợ Rãy","Đại học Sài Gòn","BHD Star","Ktx Đại học Sài Gòn","McDonald's",
                "KFC","Thảo cầm viên","Dinh Độc Lập","Công viên Tao Đàn","Nhà thờ","Bảo tàng","An Dương Vương",]
destination_buttons = []

image_paths = {
    "Sân bay": r"Picture\akf.png",
    "Bệnh viện Chợ Rãy": r"Picture\dfkr.png",
    "Đại học Sài Gòn": r"Picture\dhh.png",
    "An Dương Vương": r"Picture\fbf.png",
    "BHD Star": r"Picture\fbh.png",
    "Nhà thờ": r"Picture\fbtur.png",
    "Bảo tàng": r"Picture\gbg.png",
    "Sân bay": r"Picture\OIG.png",
    "Ktx Đại học Sài Gòn": r"Picture\OIG1.png",
    "McDonald's": r"Picture\OIGee.png",
    "Thảo cầm viên": r"Picture\rth.png",
    "Dinh Độc Lập": r"Picture\juu.png",
    "Công viên Tao Đàn": r"Picture\hph.png",
    "KFC": r"Picture\jjj.png", 
}

location_info = {
    "An Dương Vương": {"price": "$120", "rooms": 1},
    "BHD Star": {"price": "$210", "rooms": 3},
    "Sân bay": {"price": "$520", "rooms": 2},
    "Bệnh viện Chợ Rãy": {"price": "$300", "rooms": 4},
    "Đại học Sài Gòn": {"price": "$20", "rooms": 2},
    "2 Bis": {"price": "$320", "rooms": 3},
    "Nhà thờ": {"price": "$20", "rooms": 2},
    "Bảo tàng": {"price": "$100", "rooms": 2},
    "Ktx Đại học Sài Gòn": {"price": "$10", "rooms": 6},
    "McDonald's": {"price": "$100", "rooms": 1},
    "Thảo cầm viên": {"price": "$10", "rooms": 1},
    "Dinh Độc Lập": {"price": "$10", "rooms": 1},
    "Công viên Tao Đàn": {"price": "$50", "rooms": 2},
    "KFC": {"price": "$60", "rooms": 3}, 
}

scrollable_dest_frame = CTkScrollableFrame(root, label_text="Hotel")
scrollable_dest_frame.configure(height=500)
scrollable_dest_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=18, columnspan=1, sticky="nsew")
destination_images = {destination: ImageTk.PhotoImage(Image.open(path).resize((80, 80))) for destination, path in
                      image_paths.items()}

for i, destination in enumerate(destinations):
    button = ctk.CTkButton(
        scrollable_dest_frame,
        text="",  # Empty text for now
        compound="top",  # Display image above the text
        image=destination_images.get(destination),
    )
    button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    destination_buttons.append(button)

    # Add room and price information to the button text
    info = location_info.get(destination, {})
    original_text = destination  # Store the original text
    extended_text = f"{destination}\nPhòng: {info.get('rooms', 'N/A')}\nGiá: {info.get('price', 'N/A')}"
    button.configure(text=extended_text)
    
    # Store the original text in a separate attribute
    button.original_text = original_text

result_label = ctk.CTkLabel(root, text="", justify="left", anchor="w", padx=10, wraplength=400, font=("Helvetica", 14))
result_label.grid(row=14, column=2, padx=5, pady=5,sticky="w")

##Filters
filter_frame = ctk.CTkFrame(root)
filter_frame.grid(row=0, column=4, padx=5, pady=5, rowspan=14, sticky="nsew")

# Add filter options for price and rooms
price_filter_label = CTkLabel(filter_frame, text="Filter by Price:")
price_filter_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

price_options = ["Any", "$10 - $50", "$50 - $100", "$100 - $200", ">$200"]
price_combobox = CTkComboBox(filter_frame, values=price_options)
price_combobox.grid(row=0, column=5, padx=5, pady=5)

price_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

rooms_filter_label = CTkLabel(filter_frame, text="Filter by Rooms:")
rooms_filter_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")

rooms_options = ["Any", "1", "2", "3", ">3"]
rooms_combobox = CTkComboBox(filter_frame, values=rooms_options)
rooms_combobox.grid(row=1, column=5, padx=5, pady=5)

rooms_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

# Add search
search_label = CTkLabel(filter_frame, text="Search:")
search_label.grid(row=2, column=4, padx=5, pady=5, sticky="w")

search_entry = ctk.CTkEntry(filter_frame)
search_entry.grid(row=2, column=5, padx=5, pady=5, sticky="w")

# Bind the key release event to the apply_filters function
search_entry.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

# Update the apply_filter_button command to remove the lambda function
apply_filter_button = CTkButton(
    filter_frame,
    text="Apply Filters",
    command=lambda: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get())
)
apply_filter_button.grid(row=3, column=4, columnspan=2, pady=5)


# Sort options
sort_options_label = CTkLabel(filter_frame, text="Sort by:")
sort_options_label.grid(row=4, column=4, padx=5, pady=5, sticky="w")

sort_options = ["None", "Name (A to Z)", "Name (Z to A)", "Price (Low to High)", "Price (High to Low)", "Rooms (Low to High)", "Rooms (High to Low)"]
sort_combobox = CTkComboBox(filter_frame, values=sort_options)
sort_combobox.grid(row=4, column=5, padx=5, pady=5)

# Bind the key release event to the apply_filters function
# sort_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

sort_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))


def sort_destinations(destinations, sort_option):
    if sort_option == "Name (A to Z)":
        return sorted(destinations)
    elif sort_option == "Name (Z to A)":
        return sorted(destinations, reverse=True)
    elif sort_option == "Price (Low to High)":
        return sorted(destinations, key=lambda x: int(location_info[x]["price"].replace("$", "").strip()))
    elif sort_option == "Price (High to Low)":
        return sorted(destinations, key=lambda x: int(location_info[x]["price"].replace("$", "").strip()), reverse=True)
    elif sort_option == "Rooms (Low to High)":
        return sorted(destinations, key=lambda x: int(location_info[x]["rooms"]))
    elif sort_option == "Rooms (High to Low)":
        return sorted(destinations, key=lambda x: int(location_info[x]["rooms"]), reverse=True)
    else:
        return destinations








def apply_filters(price_filter, rooms_filter, keyword_filter):
    # Clear the canvas before applying filters
    # Logic to filter locations based on price and rooms
    filtered_destinations = filter_locations(price_filter, rooms_filter, keyword_filter)
    # Sort the filtered destinations based on the selected sorting option
    sorted_destinations = sort_destinations(filtered_destinations, sort_combobox.get())
    # Update destination buttons with filtered and sorted destinations
    update_destination_buttons(sorted_destinations, price_filter, rooms_filter)
    # Redraw the graph with the updated filters


# Function to filter locations based on price and rooms
def filter_locations(price_filter, rooms_filter, keyword_filter):
    filtered_destinations = []
    for destination, info in location_info.items():
        price = info.get("price", "").replace("$", "").strip()
        rooms = str(info.get("rooms", ""))
        keyword = destination.lower()

        # Check if the location meets the selected filters and keyword
        if (
            (price_filter == "Any" or check_price_filter(price, price_filter)) and
            (rooms_filter == "Any" or check_rooms_filter(rooms, rooms_filter)) and
            (keyword_filter.lower() in keyword)
        ):
            filtered_destinations.append(destination)

    return filtered_destinations

# Check price
def check_price_filter(location_price, filter_option):
    if filter_option == "Any":
        return True

    # Remove "$" sign and extra spaces if present
    location_price = location_price.replace("$", "").strip()

    # Remove any non-numeric characters from the filter option
    filter_option = ''.join(char for char in filter_option if char.isdigit() or char in ['-', '>'])

    if "-" in filter_option:
        min_price, max_price = map(int, filter_option.split("-"))
        return min_price <= int(location_price) <= max_price
    elif filter_option.startswith(">"):
        min_price = int(filter_option[1:])
        return int(location_price) > min_price
    else:
        return False
# Check room
def check_rooms_filter(location_rooms, filter_option):
    if filter_option == "Any":
        return True

    if filter_option.startswith(">"):
        min_rooms = int(filter_option[1:])
        return int(location_rooms) > min_rooms
    else:
        return location_rooms == filter_option

def update_destination_buttons(filtered_destinations, price_filter, rooms_filter):
    for button in destination_buttons:
        # Use the original_text attribute for comparison
        destination = button.original_text

        # Check if the destination is in the filtered list
        if destination in filtered_destinations:
            button.grid()  # Show the button
        else:
            button.grid_remove()  
    
    
# Start the user interface
root.mainloop()