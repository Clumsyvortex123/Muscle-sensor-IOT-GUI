import serial
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
import csv


# Configure the serial port
serial_port = 'COM3'  # Change this to the appropriate port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# Initialize data lists
x_data = []
time_data = []

# Create the figure and axis objects
fig, ax = plt.subplots()

# Create an empty line object for plotting the data
line, = ax.plot(time_data, x_data)

# Set the plot limits
time_limit = 10  # Time limit for x-axis display (in seconds)
ax.set_xlim(0, time_limit)
ax.set_ylim(0, 100)  # Adjust the limits as needed

# Define the update function for the plot
def update_plot():
    line.set_data(time_data, x_data)
    ax.relim()
    ax.autoscale_view()
    ax.set_xlim(max(0, time_data[-1] - time_limit), time_data[-1] + 1)
    canvas.draw()

def download_data():
    # Create a CSV file and write the data up to the current point in time
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'Data'])  # Write the header row
        writer.writerows(zip(time_data, x_data))  # Write the data rows up to the current point in time

def download_data_all():
    # Create a CSV file and write all the plotted data
    with open('data_all.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'Data'])  # Write the header row
        writer.writerows(zip(time_data, x_data))  # Write the data rows

def close_application():
    # Close the serial port
    ser.close()
    # Close the application
    root.quit()


# Define the start plotting process function
def start_plotting():
    try:
        # Continuously read data and update the plot
        start_time = time.time()
        while True:
            # Read a line from the serial port
            data = ser.readline().decode().strip()

            # Split the line into x and y values
            x, _ = map(int, data.split(','))

            # Get the elapsed time
            elapsed_time = time.time() - start_time

            # Append the data to the lists
            x_data.append(x)
            time_data.append(elapsed_time)

            # Update the plot
            update_plot()
            root.update()

    except serial.SerialException:
        messagebox.showerror("Error", "Serial port error!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Data Plotter")

# Create the Matplotlib figure canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the start button
start_button = tk.Button(root, text="Start", command=start_plotting)
start_button.pack(side=tk.BOTTOM, pady=10)

# Create the download all button
download_all_button = tk.Button(root, text="Download All", command=download_data_all)
download_all_button.pack(side=tk.BOTTOM, pady=10)

# Create the end button
end_button = tk.Button(root, text="End", command=close_application)
end_button.pack(side=tk.BOTTOM, pady=10)

# Run the GUI event loop
root.mainloop()

# Close the serial port
ser.close()
