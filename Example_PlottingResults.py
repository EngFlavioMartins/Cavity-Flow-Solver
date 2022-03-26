import matplotlib.pyplot as plt
from uiLibs.plot_results import plot_velocity_field # import a lib developed specifically for this project

# Select file:
backup_file = 'C:/Users/flavi/Desktop/Results/outputs_9.npz'

plot_velocity_field(backup_file)
plt.show()