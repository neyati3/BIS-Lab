import random
import math
cities = {
    "A": (0, 0),
    "B": (2, 6),
    "C": (5, 3),
    "D": (6, 7),
    "E": (8, 2),
    "F": (1, 4)
}
city_names = list(cities.keys())
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.1
random.seed(42) 
def distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
def route_distance(route):
    total = 0
    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])
    total += distance(route[-1], route[0])
    return total
def create_population():
    population = []
    for _ in range(POPULATION_SIZE):
        route = random.sample(city_names, len(city_names))
        population.append(route)
    return population
def select_parent(population):
    contestants = random.sample(population, 5)
    winner = min(contestants, key=route_distance)
    return winner
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]
    parent2_order = parent2[end + 1:] + parent2[:end + 1]
    empty_positions = (
        list(range(end + 1, size))
        + list(range(0, start))
    )
    remaining_cities = [
        city for city in parent2_order if city not in child
    ]
    for position, city in zip(empty_positions, remaining_cities):
        child[position] = city
    return child
def mutate(route):
    route = route.copy()
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route
def genetic_algorithm():
    population = create_population()
    best_route = min(population, key=route_distance).copy()
    for generation in range(GENERATIONS):
        population.sort(key=route_distance)
        if route_distance(population[0]) < route_distance(best_route):
            best_route = population[0].copy()
        new_population = [best_route.copy()]
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
        if (generation + 1) % 100 == 0:
            print(
                f"Generation {generation + 1}: "
                f"Best distance = {route_distance(best_route):.2f}"
            )
    return best_route
best_route = genetic_algorithm()
complete_route = best_route + [best_route[0]]
print("\nBest route found:")
print(" -> ".join(complete_route))
print(f"Total distance: {route_distance(best_route):.2f}")
