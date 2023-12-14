import numpy as np
import skfuzzy as fuzz
import PySimpleGUI as sg
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Creating fuzzy sets
taste = ctrl.Antecedent(np.arange(0, 11, 1), 'taste')
spiciness = ctrl.Antecedent(np.arange(0, 11, 1), 'spiciness')
temperature = ctrl.Antecedent(np.arange(0, 11, 1), 'temperature')
sweetness = ctrl.Antecedent(np.arange(0, 11, 1), 'sweetness')

usefulness = ctrl.Consequent(np.arange(0, 101, 1), 'usefulness')

# Defining membership
taste['poor'] = fuzz.trapmf(taste.universe, [0, 1, 3, 5])
taste['average'] = fuzz.trapmf(taste.universe, [2, 4, 5, 7])
taste['good'] = fuzz.trapmf(taste.universe, [5, 8, 10, 10])

spiciness['low'] = fuzz.trimf(spiciness.universe, [0, 3, 5])
spiciness['medium'] = fuzz.trimf(spiciness.universe, [3, 5, 7])
spiciness['high'] = fuzz.trimf(spiciness.universe, [5, 7, 10])


temperature['cold'] = fuzz.gaussmf(temperature.universe, 2, 1)
temperature['warm'] = fuzz.gaussmf(temperature.universe, 5, 1)
temperature['hot'] = fuzz.gaussmf(temperature.universe, 8, 1)


sweetness['low'] = fuzz.trapmf(sweetness.universe, [0, 1, 3, 5])
sweetness['medium'] = fuzz.trapmf(taste.universe, [2, 4, 5, 7])
sweetness['high'] = fuzz.trapmf(sweetness.universe, [5, 8, 10, 10])

# Defining membership functions for usefulness
usefulness['not_useful'] = fuzz.trimf(usefulness.universe, [0, 0, 50])
usefulness['moderately_useful'] = fuzz.trimf(usefulness.universe, [0, 50, 100])
usefulness['very_useful'] = fuzz.trimf(usefulness.universe, [50, 100, 100])

# Creating inference rules
rule = ctrl.Rule(taste['good'],usefulness['very_useful'])
rule1 = ctrl.Rule(taste['good'] & (spiciness['medium'] | spiciness['low']) | (sweetness['medium'] | sweetness['low']),
                  usefulness['very_useful'])
rule2 = ctrl.Rule(taste['good'] & (sweetness['high'] | spiciness['high']), usefulness['moderately_useful'])
rule3 = ctrl.Rule(taste['good'] & temperature['cold'], usefulness['moderately_useful'])
rule4 = ctrl.Rule(taste['good'] & (temperature['warm'] | temperature['hot']), usefulness['very_useful'])
rule5 = ctrl.Rule(taste['average'] & (sweetness['medium'] | spiciness['medium']) & (temperature['warm'] | temperature['hot']),
                  usefulness['moderately_useful'])
rule6 = ctrl.Rule(taste['average'] & (temperature['cold'] | temperature['warm']), usefulness['not_useful'])
rule7 = ctrl.Rule(taste['average'] & temperature['hot'], usefulness['moderately_useful'])
rule8 = ctrl.Rule(taste['poor'], usefulness['not_useful'])
rule9 = ctrl.Rule(sweetness['high'] & spiciness['high'],usefulness['not_useful'])
rule10 = ctrl.Rule(sweetness['high'] | spiciness['high'], usefulness['moderately_useful'])
rule11 = ctrl.Rule(taste['poor'] | sweetness['low'] | spiciness['low'] | temperature['cold'], usefulness['not_useful'])
rule12 = ctrl.Rule(temperature['hot'], usefulness['very_useful'])
rule13 = ctrl.Rule(temperature['warm'] & (sweetness['low'] | spiciness['low']), usefulness['not_useful'])




# Creating the inference system
evaluation_system = ctrl.ControlSystem([rule1, rule2, rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12])
food_evaluation = ctrl.ControlSystemSimulation(evaluation_system)

# Inputting values for food characteristics
#food_evaluation.input['taste'] = 6.0
#food_evaluation.input['spiciness'] = 4.5
#food_evaluation.input['temperature'] = 4.5
#food_evaluation.input['sweetness'] = 7

layout = [
    [sg.Text('Fuzzy Food Evaluation')],
    [sg.Text('Taste:'), sg.Slider(range=(0, 10), orientation='h', size=(20, 10), key='taste')],
    [sg.Text('Spiciness:'), sg.Slider(range=(0, 10), orientation='h', size=(20, 10), key='spiciness')],
    [sg.Text('Temperature:'), sg.Slider(range=(0, 10), orientation='h', size=(20, 10), key='temperature')],
    [sg.Text('Sweetness:'), sg.Slider(range=(0, 10), orientation='h', size=(20, 10), key='sweetness')],
    [sg.Button('Evaluate'), sg.Button('Exit')],
]
# Computing the usefulness of the food
#food_evaluation.compute()

# Displaying the results
#print("Usefulness of the food:", food_evaluation.output['usefulness'])

#plt.show()
window = sg.Window('Fuzzy Food Evaluation', layout)
# Event loop to handle GUI events
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    if event == 'Evaluate':
        # Set input values from the GUI
        food_evaluation.input['taste'] = values['taste']
        food_evaluation.input['spiciness'] = values['spiciness']
        food_evaluation.input['temperature'] = values['temperature']
        food_evaluation.input['sweetness'] = values['sweetness']

        # Compute the usefulness of the food

        food_evaluation.compute()
        #usefulness.view(sim=food_evaluation, backend='matplotlib')
        #spiciness.view(sim=food_evaluation, backend='matplotlib')
        #sweetness.view(sim=food_evaluation, backend='matplotlib')
        #temperature.view(sim=food_evaluation, backend='matplotlib')
        #taste.view(sim=food_evaluation, backend='matplotlib')
        # Display the results
        sg.popup(f"Usefulness of the food: {food_evaluation.output['usefulness']}")

# Close the GUI window
window.close()




## For testing purposes,

# Defining a dataset for fuzzy food characteristics
taste_data = np.array([3, 7, 8, 4, 6, 9, 2, 5, 8, 6])
spiciness_data = np.array([2, 5, 7, 3, 4, 8, 1, 4, 6, 5])
consistency_data = np.array([1, 4, 6, 2, 3, 7, 1, 3, 5, 4])
sweetness_data = np.array([4, 8, 9, 5, 7, 9, 3, 6, 9, 7])

# Plotting the dataset
plt.figure(figsize=(10, 6))

plt.subplot(221)
plt.plot(taste_data, label='Taste')
plt.title('Taste')
plt.legend()

plt.subplot(222)
plt.plot(spiciness_data, label='Spiciness')
plt.title('Spiciness')
plt.legend()

plt.subplot(223)
plt.plot(consistency_data, label='Temperature')
plt.title('Temperature')
plt.legend()

plt.subplot(224)
plt.plot(sweetness_data, label='Sweetness')
plt.title('Sweetness')
plt.legend()

plt.tight_layout()
#plt.show()
