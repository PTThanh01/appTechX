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

sort_options = ["None", "Name (A - Z)", "Name (Z - A)", "Price (Low - High)", "Price (High - Low)", "Rooms (Low - High)", "Rooms (High - Low)"]

sort_combobox = CTkComboBox(filter_frame, values=sort_options)
sort_combobox.grid(row=4, column=5, padx=5, pady=5)

# Bind the key release event to the apply_filters function
# sort_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))
sort_combobox.bind("<<ComboboxSelected>>", lambda event: update_destination_buttons(None, None, None))

def bubble_sort_buttons_by_info(buttons, sort_by):
    n = len(buttons)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            button_j = buttons[j]
            button_j1 = buttons[j + 1]

            # Check if button_j and button_j1 are CTkButton objects
            if isinstance(button_j, ctk.CTkButton) and isinstance(button_j1, ctk.CTkButton):
                info_j = location_info[button_j.original_text]
                info_j1 = location_info[button_j1.original_text]

                if sort_by == "Name":
                    name_j = button_j.original_text
                    name_j1 = button_j1.original_text

                    if name_j > name_j1:
                        buttons[j], buttons[j + 1] = buttons[j + 1], buttons[j]
                elif sort_by == "Price":
                    price_j = int(info_j["price"].replace("$", "").strip()) if info_j.get("price") else float("inf")
                    price_j1 = int(info_j1["price"].replace("$", "").strip()) if info_j1.get("price") else float("inf")

                    if price_j > price_j1:
                        buttons[j], buttons[j + 1] = buttons[j + 1], buttons[j]
                elif sort_by == "Rooms":
                    rooms_j = int(info_j["rooms"]) if info_j.get("rooms") else float("inf")
                    rooms_j1 = int(info_j1["rooms"]) if info_j1.get("rooms") else float("inf")

                    if rooms_j > rooms_j1:
                        buttons[j], buttons[j + 1] = buttons[j + 1], buttons[j]

def sort_destinations(destinations, sort_option):
    if sort_option == "None":
        return destinations
    elif sort_option == "Name (A - Z)":
        bubble_sort_buttons_by_info(destinations, "Name")
    elif sort_option == "Name (Z - A)":
        bubble_sort_buttons_by_info(destinations, "Name")
        destinations.reverse()
    elif sort_option == "Price (Low - High)":
        bubble_sort_buttons_by_info(destinations, "Price")
    elif sort_option == "Price (High - Low)":
        bubble_sort_buttons_by_info(destinations, "Price")
        destinations.reverse()
    elif sort_option == "Rooms (Low - High)":
        bubble_sort_buttons_by_info(destinations, "Rooms")
    elif sort_option == "Rooms (High - Low)":
        bubble_sort_buttons_by_info(destinations, "Rooms")
        destinations.reverse()

    return destinations



def apply_filters(price_filter, rooms_filter, keyword_filter):
    # Logic to filter locations based on price and rooms
    filtered_destinations = filter_locations(price_filter, rooms_filter, keyword_filter)

    # Sort the destinations based on the selected sorting option
    sorted_destinations = sort_destinations(filtered_destinations, sort_combobox.get())

    # Update destination buttons with sorted destinations (whether filtered or not)
    update_destination_buttons(sorted_destinations, price_filter, rooms_filter)



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

def update_destination_buttons(sorted_destinations, price_filter, rooms_filter):
    # Create a copy of the destination_buttons list to avoid modifying the original list
    sorted_buttons = destination_buttons.copy()

    # Sort the buttons based on the selected sorting option
    sort_option = sort_combobox.get()
    bubble_sort_buttons_by_info(sorted_buttons, sort_option)

    # Hide all buttons first
    for button in sorted_buttons:
        button.grid_remove()

    # Update buttons based on sorted destinations
    for i, button in enumerate(sorted_buttons):
        if sorted_destinations is not None and button.original_text in sorted_destinations:
            button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    
    
# Start the user interface
root.mainloop()