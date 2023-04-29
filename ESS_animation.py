import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Hawk:
    def __init__(self):
        self.type = "Hawk"

    def __repr__(self):
        return self.type

    def __eq__(self, other):
        if isinstance(other, Hawk):
            return True
        return False

    def __hash__(self):
        return hash(self.type)

class Dove:
    def __init__(self):
        self.type = "Dove"

    def __repr__(self):
        return self.type

    def __eq__(self, other):
        if isinstance(other, Dove):
            return True
        return False

    def __hash__(self):
        return hash(self.type)
    
    
rewards = {
    (Hawk(), Hawk()): (50, 0),  # Hawk vs Hawk: winner gets 50, loser gets 0
    (Dove(), Dove()): (40, -10),   # Dove vs Dove: winner gets 40, loser loses 10 for wasting time
    (Hawk(), Dove()): (50, -10),
    (Dove(), Hawk()): (-10, 50),  # Hawk vs Dove: winner gets 50, loser loses 10 for wasting time
}
# Counters for Hawks and Doves
hawk_points = 0
dove_points = 0



def interact(entity1, entity2):
    global hawk_points,dove_points
    reward1, reward2 = rewards.get((entity1, entity2), (0, 0))

    if entity1 == Hawk() and entity2 == Hawk():
        # Increase penalty for injured hawk
        if random.random() < 0.2:
            if reward1 >0:
                  # 20% chance of injury
                reward1 -= 100
            else :
                reward2 -= 100

    if reward1 > 0:
        if entity1 == Hawk():
            hawk_points += 1
        else:
            dove_points += 1

    if reward2 > 0:
        if entity2 == Hawk():
            hawk_points += 1
        else:
            dove_points += 1
    return reward1, reward2

# Create environment and randomly distribute points
size = 100
dove_points = np.random.rand(size, 2)
hawk_points = np.random.rand(size, 2)
colors = ["blue"] * size + ["red"] * size
points = np.concatenate([dove_points, hawk_points])
initial_points = np.copy(points)

# Set initial population
for i in range(50):
    points[i] = hawk_points[i]
for i in range(50, 100):
    points[i] = dove_points[i]



# Create figure
fig, ax = plt.subplots()

# Plot points
scatter = ax.scatter(points[:, 0], points[:, 1], c=colors)

dove_counter = 0
hawk_counter = 0

dove_text = ax.text(0.05, 0.95, "Doves: {}".format(dove_counter),
                    transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
hawk_text = ax.text(0.05, 0.90, "Hawks: {}".format(hawk_counter),
                    transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
i = 0

hawk_avg = 0
dove_avg = 0

def update(frame):
    global dove_counter, hawk_counter,i,dove_avg,hawk_avg
    
    # Interact random entities
    
    
    entity1 = random.choice([Hawk(), Dove()])
    entity2 = random.choice([Hawk(), Dove()])
    index1 = random.randint(0, size - 1)
    index2 = random.randint(size, 2 * size - 1)
    reward1, reward2 = interact(entity1, entity2)
    
    if entity1 == Dove():
        dove_counter += reward1
    elif entity1 == Hawk():
        hawk_counter += reward1
        
    if entity2 == Dove():
        dove_counter += reward2
    elif entity2 == Hawk():
        hawk_counter += reward2
        
    # Update scatter plot colors
    if reward1 > 0:
        colors[index1] = "green"
    elif reward2 > 0:
        colors[index2] = "green"
        
    scatter.set_color(colors)
    
    # Update scatter plot
    scatter.set_offsets(points)
    
    # Update counters
    dove_text.set_text("Doves: {}".format(dove_counter))
    hawk_text.set_text("Hawks: {}".format(hawk_counter))

   
    i+=1 
    hawk_avg = hawk_counter/i
    dove_avg = dove_counter/i

    return scatter, dove_text, hawk_text

# Create animation
ani = FuncAnimation(fig, update, frames=100, blit=True)

plt.show()

print("Number of interactions run in the simulation: ", i)

print("Average payoff for hawks: ", hawk_avg)
print("Average payoff for doves: ", dove_avg)
