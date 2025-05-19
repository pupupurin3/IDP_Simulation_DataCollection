import tkinter as tk
from tkinter import filedialog
import csv
from mars_simulation import MarsSimulation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MarsSimulationGUI:
    def __init__(self, root):
        self.simulation = MarsSimulation(initial_population=100)
        self.root = root
        self.root.title("Mars Population Simulation")

        # Main layout
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.side_menu = tk.Frame(root, width=200, bg="lightgray")
        self.side_menu.pack(side=tk.RIGHT, fill=tk.Y)

        # Output and canvas
        self.output_label = tk.Label(self.main_frame, text="Click 'Next Month' to start the simulation.", justify="left")
        self.output_label.pack(pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=400, height=200, bg="white")
        self.canvas.pack(pady=10)

        self.next_month_button = tk.Button(self.main_frame, text="Next Month", command=self.simulate_next_month)
        self.next_month_button.pack(pady=5)

        self.reset_button = tk.Button(self.main_frame, text="Reset Simulation", command=self.reset_simulation)
        self.reset_button.pack(pady=5)

        self.save_button = tk.Button(self.main_frame, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack(pady=5)

        # Initialize matplotlib figure
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Population and Health Over Time")
        self.ax.set_xlabel("Months")
        self.ax.set_ylabel("Values")
        self.population_line, = self.ax.plot([], [], label="Population", color="blue")
        self.health_line, = self.ax.plot([], [], label="Average Health", color="green")
        self.ax.legend()

        self.graph_canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.graph_canvas.get_tk_widget().pack(pady=10)

        # Data for the graph
        self.months = []
        self.population_data = []
        self.health_data = []

        # Side menu for parameters
        self.add_side_menu()

    def add_side_menu(self):
        tk.Label(self.side_menu, text="Simulation Parameters", bg="lightgray", font=("Arial", 14, "bold")).pack(pady=10)

        # Initial population
        tk.Label(self.side_menu, text="Initial Population:", bg="lightgray", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.initial_population_entry = tk.Entry(self.side_menu)
        self.initial_population_entry.insert(0, "100")
        self.initial_population_entry.pack(padx=10, pady=5)

        # Water usage rate (min and max)
        tk.Label(self.side_menu, text="Water Usage Rate:", bg="lightgray", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        water_frame = tk.Frame(self.side_menu, bg="lightgray")
        water_frame.pack(padx=10, pady=5, fill="x")
        tk.Label(water_frame, text="Min:", bg="lightgray").grid(row=0, column=0, padx=5)
        self.water_usage_min_entry = tk.Entry(water_frame, width=5)
        self.water_usage_min_entry.insert(0, "5")
        self.water_usage_min_entry.grid(row=0, column=1, padx=5)
        tk.Label(water_frame, text="Max:", bg="lightgray").grid(row=0, column=2, padx=5)
        self.water_usage_max_entry = tk.Entry(water_frame, width=5)
        self.water_usage_max_entry.insert(0, "15")
        self.water_usage_max_entry.grid(row=0, column=3, padx=5)

        # Hunger increase rate (min and max)
        tk.Label(self.side_menu, text="Hunger Increase Rate:", bg="lightgray", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        hunger_frame = tk.Frame(self.side_menu, bg="lightgray")
        hunger_frame.pack(padx=10, pady=5, fill="x")
        tk.Label(hunger_frame, text="Min:", bg="lightgray").grid(row=0, column=0, padx=5)
        self.hunger_rate_min_entry = tk.Entry(hunger_frame, width=5)
        self.hunger_rate_min_entry.insert(0, "5")
        self.hunger_rate_min_entry.grid(row=0, column=1, padx=5)
        tk.Label(hunger_frame, text="Max:", bg="lightgray").grid(row=0, column=2, padx=5)
        self.hunger_rate_max_entry = tk.Entry(hunger_frame, width=5)
        self.hunger_rate_max_entry.insert(0, "15")
        self.hunger_rate_max_entry.grid(row=0, column=3, padx=5)

        # Apply changes button
        self.apply_button = tk.Button(self.side_menu, text="Apply Changes", command=self.apply_changes)
        self.apply_button.pack(pady=10)

    def apply_changes(self):
        try:
            initial_population = int(self.initial_population_entry.get())
            self.simulation = MarsSimulation(initial_population=initial_population)

            water_min = float(self.water_usage_min_entry.get())
            water_max = float(self.water_usage_max_entry.get())
            hunger_min = float(self.hunger_rate_min_entry.get())
            hunger_max = float(self.hunger_rate_max_entry.get())

            self.simulation.water_usage_range = [water_min, water_max]
            self.simulation.hunger_rate_range = [hunger_min, hunger_max]

            self.output_label.config(text="Parameters updated. Reset the simulation to apply changes.")
        except ValueError:
            self.output_label.config(text="Invalid input. Please check your entries.")

    def simulate_next_month(self):
        self.simulation.simulate_month()

        # Update statistics
        stats = self.simulation.get_statistics()
        self.output_label.config(text=self.simulation.get_statistics_string())

        # Update graph data
        self.months.append(stats["month"])
        self.population_data.append(stats["population_size"])
        self.health_data.append(stats["average_health"])

        # Update graph lines
        self.population_line.set_data(self.months, self.population_data)
        self.health_line.set_data(self.months, self.health_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.graph_canvas.draw()

        # Update the canvas
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")

        # Use the initial population size to calculate the grid size
        initial_population_size = int(self.initial_population_entry.get())

        # Find the closest factor pair with a ratio of approximately 1:2
        def closest_factors(n):
            best_pair = (1, n)
            best_ratio = float("inf")
            for i in range(1, int(n**0.5) + 1):
                if n % i == 0:
                    factor1, factor2 = i, n // i
                    ratio = abs(factor2 / factor1 - 2)
                    if ratio < best_ratio:
                        best_pair = (factor1, factor2)
                        best_ratio = ratio
            # Ensure the smaller value is rows and the larger value is columns
            return best_pair if best_pair[0] <= best_pair[1] else (best_pair[1], best_pair[0])

        # Calculate rows and columns for the grid
        rows, cols = closest_factors(max(initial_population_size, 1))  # Ensure at least 1x1 grid
        cell_width = 400 // cols
        cell_height = 200 // rows

        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                x0 = j * cell_width
                y0 = i * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height

                # Assign a default color for safety
                color = "darkgray"

                if index < initial_population_size:
                    if index < len(self.simulation.population):
                        individual = self.simulation.population[index]
                        if getattr(individual, "dead", False):  # Dead individuals
                            color = "red"
                        elif individual.diseased:  # Diseased individuals (priority over green)
                            color = "yellow"
                        elif individual.hunger < 20 or individual.hydration < 20:  # Starved or dehydrated
                            color = "green"
                        else:  # Healthy individuals
                            color = "blue"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def reset_simulation(self):
        self.simulation = MarsSimulation(initial_population=int(self.initial_population_entry.get()))
        self.output_label.config(text="Simulation reset. Click 'Next Month' to start again.")
        self.update_canvas()

        self.months = []
        self.population_data = []
        self.health_data = []
        self.population_line.set_data([], [])
        self.health_line.set_data([], [])
        self.graph_canvas.draw()

    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Month", "Population Size", "Average Health"])
            for month, population, health in zip(self.months, self.population_data, self.health_data):
                writer.writerow([month, population, health])

        self.output_label.config(text=f"Simulation data saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = MarsSimulationGUI(root)
    root.mainloop()
