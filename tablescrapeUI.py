from tkinter import Tk, Label, Entry, Button, messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

def scrape_iwise():
    url = url_entry.get()

    # Use webdriver.Firefox() if you prefer Firefox
    driver = webdriver.Firefox()

    driver.get(url)

    # Wait for 30 seconds to let the page fully load
    time.sleep(30)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Use soup.find or soup.select to extract your data.
    classes = soup.select('.dhx_cal_event.cal_timetable')

    # Prepare an empty list to hold all the timetable data
    timetable_data = []

    # Counter to keep track of how many classes we've processed
    class_counter = 0

    # Iterate over each class to extract time and details
    for class_ in classes:
        class_time = class_.select_one('.dhx_title').text
        details = class_.select_one('.dhx_body').text

        timetable_data.append(f"{class_time}: {details}")
        
        # Increment the counter only if the details start with a digit
        if details[0].isdigit():
            class_counter += 1

        # If we've processed 6 classes, add a day separator and reset the counter
        if class_counter == 6:
            timetable_data.append('---')  # day separator
            class_counter = 0

    # Then write your data to a file that your Rainmeter skin can read
    with open('timetable.txt', 'w') as f:
        for line in timetable_data:
            f.write(line + "\n")

    # Get the current directory
    current_directory = os.getcwd()

    # Show a success message
    messagebox.showinfo("Success", f"Written data to timetable.txt in {current_directory}")

    # Close the browser window
    driver.quit()

    # Quit the main application
    window.quit()

# Create a window
window = Tk()
window.geometry("450x100")  # Set window dimensions

# Create a label
url_label = Label(window, text="iWise URL:")
url_label.pack()

# Create a text entry box
url_entry = Entry(window, width=60)
url_entry.pack()

# Create a button that will call the scraping function when clicked
scrape_button = Button(window, text="Scrape Timetable", command=scrape_iwise)
scrape_button.pack()

# Create a 'Quit' button
quit_button = Button(window, text="Quit", command=window.quit)
quit_button.pack()

# Run the GUI
window.mainloop()
