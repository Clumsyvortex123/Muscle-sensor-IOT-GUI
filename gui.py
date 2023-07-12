import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class EMGGraphApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("EMG Data Graph")
        self.configure(background='#f0f0f0')
        

        self.emg_data = None
        self.current_index = 0
        self.time_window = 10
        self.running = False

        self.create_widgets()

    def create_widgets(self):
        # Notebook for multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create the main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")

        # Frame for the graph and table
        self.graph_frame = tk.Frame(self.main_tab, bg='#ffffff')
        self.graph_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Figure and axes for the main plot
        self.fig_main, self.ax_main = plt.subplots(figsize=(8, 6))
        self.plot_line_main = None

        # Canvas for embedding the main plot
        self.canvas_main = FigureCanvasTkAgg(self.fig_main, master=self.graph_frame)
        self.canvas_main.draw()
        self.canvas_main.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the table
        self.table_scrollbar = tk.Scrollbar(self.graph_frame)
        self.table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Table to display CSV data
        self.table = ttk.Treeview(self.graph_frame, show="headings", yscrollcommand=self.table_scrollbar.set)
        self.table_scrollbar.config(command=self.table.yview)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button for importing data from a CSV file
        self.import_button = tk.Button(self.main_tab, text="Import CSV", command=self.import_csv, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.import_button.pack(pady=10)

        # Buttons for navigating the timeline
        self.prev_button = tk.Button(self.main_tab, text="Previous", command=self.show_previous, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.main_tab, text="Next", command=self.show_next, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Button for running through all values
        self.run_button = tk.Button(self.main_tab, text="Run All", command=self.run_all_values, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Button for pausing the graph
        self.pause_button = tk.Button(self.main_tab, text="Pause", command=self.pause_graph, state=tk.DISABLED, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Create the specific timestamp tab
        self.timestamp_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.timestamp_tab, text="Specific Timestamp")

        # Frame for the timestamp inputs and button
        self.timestamp_frame = tk.Frame(self.timestamp_tab, bg='#ffffff')
        self.timestamp_frame.pack(pady=10)

        # Labels and entry fields for start and end timestamps
        self.start_label = tk.Label(self.timestamp_frame, text="Start Timestamp:", bg='#ffffff', fg='#000000')
        self.start_label.pack(side=tk.LEFT)

        self.start_entry = tk.Entry(self.timestamp_frame)
        self.start_entry.pack(side=tk.LEFT, padx=5)

        self.end_label = tk.Label(self.timestamp_frame, text="End Timestamp:", bg='#ffffff', fg='#000000')
        self.end_label.pack(side=tk.LEFT, padx=10)

        self.end_entry = tk.Entry(self.timestamp_frame)
        self.end_entry.pack(side=tk.LEFT)

        # Button to show data for specific timestamps
        self.show_data_button = tk.Button(self.timestamp_tab, text="Show Data", command=self.show_specific_timestamp, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.show_data_button.pack(pady=10)

        # Frame for the second plot
        self.second_plot_frame = tk.Frame(self.timestamp_tab, bg='#ffffff')
        self.second_plot_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Figure and axes for the second plot
        self.fig_second, self.ax_second = plt.subplots(figsize=(8, 6))
        self.plot_line_second = None

        # Canvas for embedding the second plot
        self.canvas_second = FigureCanvasTkAgg(self.fig_second, master=self.second_plot_frame)
        self.canvas_second.draw()
        self.canvas_second.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the realtime tab
        self.realtime_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.realtime_tab, text="Realtime")

        # Frame for the realtime graph
        self.realtime_frame = tk.Frame(self.realtime_tab, bg='#ffffff')
        self.realtime_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Figure and axes for the realtime plot
        self.fig_realtime, self.ax_realtime = plt.subplots(figsize=(8, 6))
        self.plot_line_realtime = None

        # Canvas for embedding the realtime plot
        self.canvas_realtime = FigureCanvasTkAgg(self.fig_realtime, master=self.realtime_frame)
        self.canvas_realtime.draw()
        self.canvas_realtime.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button to get real-time input
        self.realtime_button = tk.Button(self.realtime_tab, text="Get Realtime Input", command=self.get_realtime_input, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.realtime_button.pack(pady=10)

        # Button to download realtime data
        self.download_button = tk.Button(self.realtime_tab, text="Download Data", command=self.download_realtime_data, bg='#ffffff', fg='#000000', relief=tk.RAISED)
        self.download_button.pack(pady=10)

    def get_realtime_input(self):
        # Code to get realtime input from OYmotion analog muscle sensor
        # Update the realtime graph with the received data
        pass

    def download_realtime_data(self):
        if self.realtime_data:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                df = pd.DataFrame(self.realtime_data)
                df.to_csv(filename, index=False)
                print("Realtime data downloaded successfully.")


    def import_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.emg_data = pd.read_csv(filename)
            self.current_index = 0
            self.plot_graph()
            self.display_data_table()

    def show_previous(self):
        if self.emg_data is not None and self.current_index > 0:
            self.current_index -= 1
            self.update_graph()

    def show_next(self):
        if self.emg_data is not None and self.current_index < len(self.emg_data) - 1:
            self.current_index += 1
            self.update_graph()

    def plot_graph(self):
        if self.emg_data is not None:
            self.ax_main.clear()
            self.plot_line_main = self.ax_main.plot(self.emg_data["Time"], self.emg_data.iloc[:, 1:], linewidth=1)
            self.ax_main.set_title("EMG Data")
            self.ax_main.set_xlabel("Time")
            self.ax_main.set_ylabel("Amplitude")
            self.update_xaxis_limits_main()
            self.canvas_main.draw()

    def update_graph(self):
        if self.emg_data is not None and self.plot_line_main is not None:
            self.update_xaxis_limits_main()
            self.canvas_main.draw()

    def update_xaxis_limits_main(self):
        start_index = max(0, self.current_index - self.time_window)
        end_index = min(len(self.emg_data), self.current_index + self.time_window + 1)
        x_min = self.emg_data["Time"][start_index]
        x_max = self.emg_data["Time"][end_index - 1]
        self.ax_main.set_xlim(x_min, x_max)

    def run_all_values(self):
        if self.emg_data is not None and not self.running:
            self.running = True
            self.pause_button.config(state=tk.NORMAL)
            self.run_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.run_values_recursive()

    def run_values_recursive(self):
        if self.current_index < len(self.emg_data) and self.running:
            self.update_graph()
            self.update_idletasks()
            self.current_index += 1
            self.after(100, self.run_values_recursive)
        else:
            self.running = False
            self.pause_button.config(state=tk.DISABLED)
            self.run_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)

    def pause_graph(self):
        if self.running:
            self.running = False
            self.pause_button.config(text="Resume")
        else:
            self.running = True
            self.pause_button.config(text="Pause")
            self.run_values_recursive()

    def display_data_table(self):
        if self.emg_data is not None:
            columns = list(self.emg_data.columns)
            self.table["columns"] = columns

            for column in columns:
                self.table.heading(column, text=column)
                self.table.column(column, width=100, anchor=tk.CENTER)

            for index, row in self.emg_data.iterrows():
                values = list(row)
                self.table.insert("", tk.END, values=values)

    def show_specific_timestamp(self):
        if self.emg_data is not None:
            start_timestamp = float(self.start_entry.get())
            end_timestamp = float(self.end_entry.get())

            mask = (self.emg_data["Time"] >= start_timestamp) & (self.emg_data["Time"] <= end_timestamp)
            specific_data = self.emg_data[mask]

            self.ax_second.clear()
            self.ax_second.plot(specific_data["Time"], specific_data.iloc[:, 1:], linewidth=1)
            self.ax_second.set_title("EMG Data - Specific Timestamp")
            self.ax_second.set_xlabel("Time")
            self.ax_second.set_ylabel("Amplitude")
            self.canvas_second.draw()

    def destroy(self):
        plt.close('all')
        tk.Tk.destroy(self)

app = EMGGraphApp()
app.mainloop()
