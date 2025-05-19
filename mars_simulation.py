import random

class Individual:
    def __init__(self, age=0, health=100, hydration=100, hunger=100, diseased=False):
        self.age = age
        self.health = health
        self.hydration = hydration
        self.hunger = hunger
        self.diseased = diseased
        self.dead = False

    def age_one_month(self):
        if self.dead:
            return

        # Age and degrade health
        self.age += 1 / 12
        self.hydration -= random.uniform(5, 15)
        self.hunger -= random.uniform(5, 15)

        # Check for starvation or dehydration
        if self.hydration < 20 or self.hunger < 20:
            self.health -= 10  # Severe penalty for starvation/dehydration

        # Recover hydration and hunger if above threshold
        if self.hydration >= 50 and self.hunger >= 50:
            self.health += 5  # Gradual recovery

        # Disease recovery based on health level
        if self.diseased:
            recovery_chance = (self.hydration + self.hunger) / 200
            if random.random() < recovery_chance:
                self.diseased = False

        # Check for death
        if self.health <= 0:
            self.dead = True

class MarsSimulation:
    def __init__(self, initial_population=100):
        self.population = [Individual() for _ in range(initial_population)]
        self.month = 0

    def simulate_month(self):
        self.month += 1
        for individual in self.population:
            individual.age_one_month()

    def get_statistics(self):
        total_health = sum(ind.health for ind in self.population if not ind.dead)
        avg_health = total_health / len(self.population) if self.population else 0
        diseased_count = sum(1 for ind in self.population if ind.diseased)
        return {
            "month": self.month,
            "population_size": len(self.population),
            "average_health": avg_health,
            "diseased_count": diseased_count,
        }

    def get_statistics_string(self):
        stats = self.get_statistics()
        return (f"Month {stats['month']}: Population = {stats['population_size']}, "
                f"Avg Health = {stats['average_health']:.2f}, Diseased = {stats['diseased_count']}")

    def run_simulation(self, months=120):
        for _ in range(months):
            self.simulate_month()
            stats = self.get_statistics()
            print(f"Month {stats['month']}: Population = {stats['population_size']}, Avg Health = {stats['average_health']:.2f}, Diseased = {stats['diseased_count']}")

if __name__ == "__main__":
    sim = MarsSimulation(initial_population=100)
    sim.run_simulation(months=120)
