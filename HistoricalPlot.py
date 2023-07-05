import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class ScatterPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scatter Plot App")

        # Create GUI elements
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Read data from CSV file
        self.read_data_from_csv('EMG_data.csv')

        # Create scatter plot tab
        self.create_scatter_plot_tab()

    def read_data_from_csv(self, csv_file_path):
        self.data = []
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                self.data.append((float(row[0]), float(row[1])))

    def create_scatter_plot_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Scatter Plot")

        # Create a Figure object and initialize empty data
        self.figure = Figure(figsize=(6, 4))
        self.plot = self.figure.add_subplot(111)
        self.current_segment = 0

        # Create GUI elements
        self.canvas = FigureCanvasTkAgg(self.figure, master=tab)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.prev_button = tk.Button(tab, text="Previous", command=self.show_previous_segment)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.next_button = tk.Button(tab, text="Next", command=self.show_next_segment)
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Display the initial segment
        self.show_segment(self.current_segment)

    def show_segment(self, segment):
        segment_data = self.data[segment * 100 : (segment + 1) * 100]
        x_values = [data[0] for data in segment_data]
        y_values = [data[1] for data in segment_data]

        self.plot.clear()
        self.plot.plot(x_values, y_values, 'bo-')
        self.plot.set_xlabel('X-axis')
        self.plot.set_ylabel('Y-axis')
        self.plot.set_title('Scatter Plot (Segment {})'.format(segment))
        self.plot.grid(True)
        self.canvas.draw()

    def show_previous_segment(self):
        if self.current_segment > 0:
            self.current_segment -= 1
            self.show_segment(self.current_segment)

    def show_next_segment(self):
        if self.current_segment < len(self.data) // 100 - 1:
            self.current_segment += 1
            self.show_segment(self.current_segment)

# Create the Tkinter application window
root = tk.Tk()

# Create an instance of the ScatterPlotApp class
app = ScatterPlotApp(root)

# Start the Tkinter event loop
root.mainloop()

