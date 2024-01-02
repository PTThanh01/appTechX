from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkScrollableFrame, CTkComboBox, CTkLabel, CTkButton
import locale

# Create window customtkinter
root = ctk.CTk()
root.title("Find Hotel")
root.geometry("650x600")

destinations = ["Sân bay", "Bệnh viện Chợ Rãy", "Đại học Sài Gòn", "BHD Star", "Ktx Đại học Sài Gòn", "McDonald's",
                "KFC", "Thảo cầm viên", "Dinh Độc Lập", "Công viên Tao Đàn", "Nhà thờ", "Bảo tàng", "An Dương Vương", ]
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
scrollable_dest_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=16, columnspan=1, sticky="nsew")

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
result_label.grid(row=14, column=2, padx=5, pady=5, sticky="w")

# Filters
filter_frame = ctk.CTkFrame(root)
filter_frame.grid(row=0, column=4, padx=5, pady=5, rowspan=16, sticky="nsew")

sort_name_asc_button = CTkButton(filter_frame, text="Sort by Name (A-Z)", command=lambda: bubble_sort_destinations_by_name(False))
sort_name_asc_button.grid(row=4, column=4, padx=5, pady=5)

sort_name_desc_button = CTkButton(filter_frame, text="Sort by Name (Z-A)", command=lambda: bubble_sort_destinations_by_name(True))
sort_name_desc_button.grid(row=4, column=5, padx=5, pady=5)

sort_price_asc_button = CTkButton(filter_frame, text="Sort by Price (Low to High)",
                                  command=lambda: bubble_sort_destinations_by_price(False))
sort_price_asc_button.grid(row=5, column=4, padx=5, pady=5)

sort_price_desc_button = CTkButton(filter_frame, text="Sort by Price (High to Low)",
                                   command=lambda: bubble_sort_destinations_by_price(True))
sort_price_desc_button.grid(row=5, column=5, padx=5, pady=5)


sort_filter_label = CTkLabel(filter_frame, text="Filter by Name:")
sort_filter_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

sort_name_options = ["A - Z", "Z - A"]
sort_name_combobox = CTkComboBox(filter_frame, values=sort_name_options)
sort_name_combobox.grid(row=0, column=5, padx=5, pady=5)




def bubble_sort_destinations_by_name(reverse_order=False):
    n = len(destination_buttons)
    for i in range(n):
        for j in range(0, n - i - 1):
            text_j = destination_buttons[j].cget("text")
            text_j1 = destination_buttons[j + 1].cget("text")

            # Use strcoll for locale-aware string comparison
            comparison = locale.strcoll(text_j, text_j1)

            if (not reverse_order and comparison > 0) or (reverse_order and comparison < 0):
                destination_buttons[j], destination_buttons[j + 1] = destination_buttons[j + 1], destination_buttons[j]

    update_destination_buttons([])

# Set locale to Vietnamese
locale.setlocale(locale.LC_COLLATE, 'vi_VN.UTF-8')


def bubble_sort_destinations_by_price(reverse_order=False):
    n = len(destination_buttons)
    for i in range(n):
        for j in range(0, n-i-1):
            # Extract the price from the button text
            price_j = int(destination_buttons[j].cget("text").split('\n')[-1].replace("Giá: $", ""))
            price_j1 = int(destination_buttons[j+1].cget("text").split('\n')[-1].replace("Giá: $", ""))
            if (not reverse_order and price_j > price_j1) or (reverse_order and price_j < price_j1):
                destination_buttons[j], destination_buttons[j+1] = destination_buttons[j+1], destination_buttons[j]
    update_destination_buttons([])


def update_destination_buttons(filtered_destinations):
    for i, button in enumerate(destination_buttons):
        destination = button.cget("text")

        if not filtered_destinations or destination in filtered_destinations:
            button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")  # Show the button
        else:
            button.grid_remove()  # Hide the button

# Start the user interface
root.mainloop()
