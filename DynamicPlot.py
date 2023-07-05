import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class ScatterPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Scatter Plot")

        # Create a Figure object and initialize empty data
        self.figure = Figure(figsize=(6, 4))
        self.plot = self.figure.add_subplot(111)
        self.x_values = []
        self.y_values = []
        self.line = None
        self.animating = False
        self.i = 0  # Initialize the counter

        # Create GUI elements
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.start_button = tk.Button(self.root, text="Start", command=self.start_animation)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_animation)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Read data from CSV file
        self.read_data_from_csv('EMG_data.csv')

    def read_data_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                self.x_values.append(float(row[0]))
                self.y_values.append(float(row[1]))

    def animate(self):
        if self.animating:
            self.plot.clear()
            self.plot.plot(self.x_values[:self.i], self.y_values[:self.i], 'bo-')
            self.plot.set_xlabel('X-axis')
            self.plot.set_ylabel('Y-axis')
            self.plot.set_title('Animated Scatter Plot')
            self.plot.grid(True)
            self.canvas.draw()
            self.i += 1  # Increment the counter

    def start_animation(self):
        self.animating = True
        self.line = self.plot.plot([], [], 'bo-')[0]
        self.animation = self.canvas.new_timer(interval=100)
        self.animation.add_callback(self.animate)
        self.animation.start()

    def stop_animation(self):
        self.animating = False
        if self.animation:
            self.animation.stop()

# Create the Tkinter application window
root = tk.Tk()

# Create an instance of the ScatterPlotApp class
app = ScatterPlotApp(root)

# Start the Tkinter event loop
root.mainloop()
