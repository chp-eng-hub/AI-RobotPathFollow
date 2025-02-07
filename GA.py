#!/usr/bin/env python3

import random
import csv
from deap import base, creator, tools, algorithms

def optimize_with_ga(input_csv_path, output_csv_path, population_size, generations, mutation_prob, crossover_prob, elitism):
    with open(input_csv_path, "r") as file:
        reader = csv.DictReader(file)
        points = [(float(row["X (mm)"]), float(row["Y (mm)"])) for row in reader]

    num_points = len(points)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(num_points), num_points)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        total_distance = 0
        for i in range(len(individual)):
            point1 = points[individual[i]]
            point2 = points[individual[(i + 1) % len(individual)]]  # Wrap around
            total_distance += ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        return total_distance,

    def mutate(individual):
        a, b = random.sample(range(len(individual)), 2)
        individual[a], individual[b] = individual[b], individual[a]
        return individual,

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=population_size)

    for ind in population:
        ind.fitness.values = toolbox.evaluate(ind)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fits: sum(f[0] for f in fits) / len(fits))
    stats.register("min", lambda fits: min(f[0] for f in fits))
    stats.register("max", lambda fits: max(f[0] for f in fits))

    halloffame = tools.HallOfFame(1) if elitism else None

    result_population, _ = algorithms.eaSimple(
        population, toolbox, cxpb=crossover_prob, mutpb=mutation_prob, ngen=generations,
        stats=stats, halloffame=halloffame, verbose=True
    )

    best_individual = tools.selBest(result_population, k=1)[0]

    # Calculate total distance for the best individual
    total_distance = evaluate(best_individual)[0]
    print(f"Optimization completed. Total distance: {total_distance:.2f} mm")

    optimized_points = [points[i] for i in best_individual]
    with open(output_csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X (mm)", "Y (mm)"])
        writer.writerows(optimized_points)

    print(f"Optimized coordinates saved to {output_csv_path}")

if __name__ == "__main__":
    input_csv_path = "pointset.csv"
    output_csv_path = "pointset_optimized_ga.csv"
    population_size=500
    generations=500
    mutation_prob=0.3
    crossover_prob=0.9
    elitism=True
    optimize_with_ga(input_csv_path, output_csv_path, population_size, generations, mutation_prob, crossover_prob, elitism)
