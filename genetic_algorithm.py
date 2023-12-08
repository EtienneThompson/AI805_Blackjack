import json
import random
import matplotlib.pyplot as plt
from GavenAgent import GavenAgent, generate_random_genome

# Constants
population_size = 1002
parent_selection_fraction = 0.5  # 50% of the population size
num_parents_to_select = int(population_size * parent_selection_fraction)
mutation_rate = 0.01
num_generations = 100
num_games_per_agent = 100  # Number of Blackjack games each agent will play


# Evaluate fitness
def evaluate_fitness(agent, num_games=num_games_per_agent):
    final_chip_count = play_blackjack_games(agent, num_games)
    fitness = final_chip_count  # Fitness is now the final chip count directly
    return max(fitness, 0)  # Ensure fitness is non-negative


def adjust_population_size(size):
    return size + (6 - size % 6) % 6

def save_best_genomes(best_genomes, file_name='best_genomes.json'):
    with open(file_name, 'w') as f:
        json.dump(best_genomes, f)

# Initialize population
def initialize_population(size):
    return [GavenAgent(generate_random_genome(), f"GavenAgent_{i+1}", False) for i in range(size)]

# Evaluate fitness
def evaluate_fitness(agent, num_games=num_games_per_agent):
    final_chip_count = play_blackjack_games(agent, num_games)
    fitness = final_chip_count - 1000  # Assuming each agent starts with 1000 chips
    print(f"Agent: {agent.get_name()}, Final Chips: {final_chip_count}, Fitness: {fitness}")  # Debugging line
    return max(fitness, 0)  # Ensure fitness is non-negative

# Select parents
def select_parents(population, fitness_scores, num_parents):
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
    parents = sorted_population[:num_parents // 2]
    tournament_size = 3
    while len(parents) < num_parents:
        tournament = random.sample(population, tournament_size)
        best_in_tournament = max(tournament, key=lambda agent: fitness_scores[population.index(agent)])
        parents.append(best_in_tournament)
    return parents

# Crossover
def crossover(parent1_genome, parent2_genome):
    child1_genome = {}
    child2_genome = {}
    for hand_value in parent1_genome:
        if random.random() < 0.5:
            child1_genome[hand_value] = parent1_genome[hand_value]
            child2_genome[hand_value] = parent2_genome[hand_value]
        else:
            child1_genome[hand_value] = parent2_genome[hand_value]
            child2_genome[hand_value] = parent1_genome[hand_value]
    return child1_genome, child2_genome

# Mutation
def mutate(genome, mutation_rate=mutation_rate):
    mutated_genome = genome.copy()
    for hand_value, actions in mutated_genome.items():
        if random.random() < mutation_rate:
            # Slightly modify the probabilities
            action_to_modify = random.choice(list(actions.keys()))
            actions[action_to_modify] += random.uniform(-0.1, 0.1)  # Adjust this range as needed
            # Ensure probabilities sum to 1
            total = sum(actions.values())
            mutated_genome[hand_value] = {action: prob / total for action, prob in actions.items()}
    return mutated_genome

# Create next generation
def create_next_generation(population, fitness_scores):
    new_population = []
    parents = select_parents(population, fitness_scores, num_parents_to_select)

    # Iterate over the list of parents in pairs
    for i in range(0, len(parents), 2):
        if i + 1 < len(parents):  # Check if there is a pair available
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1_genome, child2_genome = crossover(parent1.genome, parent2.genome)
            new_population.append(GavenAgent(mutate(child1_genome), parent1._name, False))
            new_population.append(GavenAgent(mutate(child2_genome), parent2._name, False))

        if len(new_population) >= len(population):  # Ensure the new population doesn't exceed the original population size
            break

    return new_population



# Play Blackjack games
def play_blackjack_games(agent, num_games):
    total_chips = 0
    for _ in range(num_games):
        # Simulate a game of blackjack here
        # Update total_chips based on the outcome of the game
        pass  # Replace this with your game simulation logic
    return total_chips

def save_best_genomes(population, fitness_scores, file_name='best_genomes.json'):
    best_genomes = [population[i].genome for i in range(len(population)) if fitness_scores[i] == max(fitness_scores)]
    with open(file_name, 'w') as f:
        json.dump(best_genomes, f)

# Main genetic algorithm loop
def run_genetic_algorithm(population_size, num_generations):
    population = initialize_population(population_size)
    average_fitness_per_generation = []  # List to store average fitness per generation

    for generation in range(num_generations):
        fitness_scores = [evaluate_fitness(agent) for agent in population]
        average_fitness = sum(fitness_scores) / len(fitness_scores)
        average_fitness_per_generation.append(average_fitness)  # Store average fitness

        new_population = create_next_generation(population, fitness_scores)
        population = new_population
        # print(f"Generation {generation + 1}/{num_generations} complete.")

    return population, fitness_scores, average_fitness_per_generation
