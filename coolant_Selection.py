import csv
import random

# Define a class to represent coolant properties
class Coolant:
    def __init__(self, name, Ja, thermal_conductivity, specific_heat, surface_tension, viscosity, cost):
        self.name = name
        self.Ja = Ja
        self.thermal_conductivity = thermal_conductivity
        self.specific_heat = specific_heat
        self.surface_tension = surface_tension
        self.viscosity = viscosity
        self.cost = cost

# Function to read coolant data from a CSV file
def read_coolant_data(file_path):
    coolants = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            coolant = Coolant(
                row['Name'], float(row['Ja']), float(row['ThermalConductivity']),
                float(row['SpecificHeat']), float(row['SurfaceTension']),
                float(row['Viscosity']), float(row['Cost'])
            )
            coolants.append(coolant)
    return coolants

# Function to normalize property values in the dataset
def normalize_data(coolants):
    properties = ['Ja', 'thermal_conductivity', 'specific_heat', 'surface_tension', 'viscosity', 'cost']
    for prop in properties:
        min_val = min(getattr(c, prop) for c in coolants)
        max_val = max(getattr(c, prop) for c in coolants)
        for coolant in coolants:
            setattr(coolant, prop, (getattr(coolant, prop) - min_val) / (max_val - min_val))
    return coolants

# Function to assign random weights for properties
def assign_random_weights(properties):
    weights = {prop: round(random.uniform(-5, 5), 2) for prop in properties}
    return weights

# Function to calculate the score of a coolant based on weighted properties
def calculate_coolant_score(coolant, weights):
    score = sum(getattr(coolant, prop) * weight for prop, weight in weights.items())
    return score

# Load coolant data from a CSV file (You should provide your CSV file)
coolant_data = read_coolant_data('coolant_data.csv')

# Normalize property values in the dataset
coolant_data = normalize_data(coolant_data)

# Split the dataset into training and testing sets
random.shuffle(coolant_data)
train_set = coolant_data[:int(0.8 * len(coolant_data))]
test_set = coolant_data[int(0.8 * len(coolant_data):)]

# Assign random weights to properties
properties = ['Ja', 'thermal_conductivity', 'specific_heat', 'surface_tension', 'viscosity', 'cost']
weights = assign_random_weights(properties)

# Initialize variables to keep track of the best coolant and its score
best_coolant = None
best_score = float('-inf')

# Evaluate each coolant in the test set
for coolant in test_set:
    score = calculate_coolant_score(coolant, weights)
    if score > best_score:
        best_score = score
        best_coolant = coolant

# Print the selected coolant and its properties
if best_coolant:
    print(f"The selected coolant is {best_coolant.name} with a score of {best_score}")
    print("Properties:")
    for prop, weight in weights.items():
        value = round(getattr(best_coolant, prop), 2)
        print(f"{prop}: {value} (Weight: {weight})")
else:
    print("No coolant selected.")
