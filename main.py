import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a random password and insert it into the password entry field."""
    
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Generate random character sequences
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

   
    password = "".join(password_list)
    
    # Clear existing entry and insert new password
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Save website, email, and password to a JSON file."""
    # Get data from entries
    website = website_entry.get().strip().capitalize()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    # Validate input fields
    if not website or not email or not password:
        messagebox.showwarning(
            title="Missing Information", 
            message="Please fill in all fields."
        )
        return

    # Create new data entry
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    try: 
            # Reading old data
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                    
    except FileNotFoundError:
            with open("data.json", "w") as data_file:    
                json.dump(new_data, data_file, indent=4)

    else:
        #    Updating old data with new data
           data.update(new_data)
           with open("data.json", "w") as data_file:
                # Saving updated data   
                json.dump(data, data_file, indent=4)
         
    finally:
            # Clear fields and show success message
                website_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                messagebox.showinfo(
                title="Success", 
                message="Credentials saved successfully!"
                )
   

    

# ------------------------------ FIND PASSWORD ---------------------------#
def find_password():
    """Search for website credentials in the data file."""
    website = website_entry.get().strip().capitalize()
    
    # Validate input
    if not website:
        messagebox.showwarning(
            title="Missing Website", 
            message="Please enter a website to search."
        )
        return

    try:
        # Try to read data file
        with open("data.json", "r") as data_file: 
            data = json.load(data_file)
        
    except FileNotFoundError:
        # Handle missing or invalid file
        messagebox.showwarning(
            title="Data Error", 
            message="No valid data file found."
        )
        return

    # Check if website exists in data
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(
            title=website, 
            message=f"Email/Username: {email}\nPassword: {password}"
        )
    else:
        messagebox.showinfo(
            title="Not Found", 
            message=f"No credentials found for {website}."
        )

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

# Create canvas with logo
canvas = tk.Canvas(height=200, width=200)
try:
    logo_img = tk.PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(row=0, column=1)


except:
    # Fallback if logo is missing
    canvas.create_text(100, 100, text="Logo", fill="black", font=("Arial", 20))
    canvas.grid(row=0, column=1)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e", padx=(0, 5), pady=5)

email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e", padx=(0, 5), pady=5)

password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e", padx=(0, 5), pady=5)

# Entries
website_entry = tk.Entry(width=24)
website_entry.grid(row=1, column=1, sticky="ew", pady=5)
website_entry.focus()

email_entry = tk.Entry(width=42)
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)
email_entry.insert(0, "osumanu@email.com")

password_entry = tk.Entry(width=24)
password_entry.grid(row=3, column=1, sticky="ew", pady=5)

# Buttons
search_button = tk.Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, sticky="ew", padx=(5, 0))

generate_password_button = tk.Button(
    text="Generate Password", width=14, command=generate_password
)
generate_password_button.grid(row=3, column=2, sticky="ew", padx=(5, 0))

add_button = tk.Button(text="Add Credentials", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="ew", pady=5)




window.mainloop()
