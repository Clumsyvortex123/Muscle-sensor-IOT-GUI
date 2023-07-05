import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class ScatterPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Combined Scatter Plot App")

        # Create GUI elements
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Read data from CSV file
        self.read_data_from_csv('EMG_data.csv')

        # Create animated scatter plot tab
        self.create_animated_scatter_plot_tab()

        # Create scatter plot tab
        self.create_scatter_plot_tab()

    def read_data_from_csv(self, csv_file_path):
        self.data = []
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                self.data.append((float(row[0]), float(row[1])))

    def create_animated_scatter_plot_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Animated Scatter Plot")

        # Create a Figure object and initialize empty data
        self.figure_anim = Figure(figsize=(6, 4))
        self.plot_anim = self.figure_anim.add_subplot(111)
        self.x_values_anim = []
        self.y_values_anim = []
        self.line_anim = None
        self.animating = False
        self.i = 0  # Initialize the counter

        # Create GUI elements
        self.canvas_anim = FigureCanvasTkAgg(self.figure_anim, master=tab)
        self.canvas_anim.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.start_button_anim = tk.Button(tab, text="Start", command=self.start_animation)
        self.start_button_anim.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_button_anim = tk.Button(tab, text="Stop", command=self.stop_animation)
        self.stop_button_anim.pack(side=tk.LEFT, padx=10, pady=10)

        # Display the initial scatter plot
        self.show_scatter_plot_anim()

    def animate(self):
        if self.animating:
            self.plot_anim.clear()
            self.plot_anim.plot(self.x_values_anim[:self.i], self.y_values_anim[:self.i], 'bo-')
            self.plot_anim.set_xlabel('X-axis')
            self.plot_anim.set_ylabel('Y-axis')
            self.plot_anim.set_title('Animated Scatter Plot')
            self.plot_anim.grid(True)
            self.canvas_anim.draw()
            self.i += 1  # Increment the counter

    def start_animation(self):
        self.animating = True
        self.line_anim = self.plot_anim.plot([], [], 'bo-')[0]
        self.animation = self.canvas_anim.new_timer(interval=100)
        self.animation.add_callback(self.animate)
        self.animation.start()

    def stop_animation(self):
        self.animating = False
        if self.animation:
            self.animation.stop()

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
        segment_data = self.data[segment * 100: (segment + 1) * 100]
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

    def show_scatter_plot_anim(self):
        self.x_values_anim = [data[0] for data in self.data]
        self.y_values_anim = [data[1] for data in self.data]

        self.plot_anim.clear()
        self.plot_anim.plot(self.x_values_anim, self.y_values_anim, 'bo-')
        self.plot_anim.set_xlabel('X-axis')
        self.plot_anim.set_ylabel('Y-axis')
        self.plot_anim.set_title('Animated Scatter Plot')
        self.plot_anim.grid(True)
        self.canvas_anim.draw()

# Create the Tkinter application window
root = tk.Tk()

# Create an instance of the ScatterPlotApp class
app = ScatterPlotApp(root)

# Start the Tkinter event loop
root.mainloop()
