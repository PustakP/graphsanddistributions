import random
import math
import matplotlib.pyplot as plt

def gaussian_distribution(mean, std_dev, num_samples):
    # Initialize an empty list to store samples
    samples = []

    # Generate samples using the Box-Muller transform
    for i in range(num_samples // 2):  # We generate two samples at a time
        # Generate two random numbers between 0 and 1
        u1 = random.random()
        u2 = random.random()

        # Apply the Box-Muller transformation
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2) # z1 and z2 are independent
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2) # box muller transformation used because it is computationally efficient

        # Scale and shift the samples to match the desired mean and standard deviation
        x1 = z1 * std_dev + mean
        x2 = z2 * std_dev + mean

        samples.append(x1)
        samples.append(x2)

    return samples[:num_samples]  # Return only the requested number of samples incase there is an odd number of samples

# Get the number of samples from user input
num_samples = int(input("Enter the number of samples: "))

# Set mean and standard deviation
mean = 0
std_dev = 1

# Generate samples
samples = gaussian_distribution(mean, std_dev, num_samples)

# Plot the distribution
fig, ax1 = plt.subplots(figsize=(8, 6))

ax1.set_xlabel('Value')
ax1.set_ylabel('Probability Density', color='g')
ax1.tick_params(axis='y', labelcolor='g')

# After plotting the histogram:
n, bins, patches = ax1.hist(samples, bins=35, density=True, alpha=0.6, color='g', label='Histogram')

# Compute the midpoints of the histogram bars
midpoints = (bins[:-1] + bins[1:]) / 2

# Compute the "convolution" as the heights of the histogram bars
convolution = n

# Plot convolution
ax2 = ax1.twinx()
ax2.plot(midpoints, convolution, color='b', label='Midpoint Line', linewidth=2)
ax2.set_ylabel('Frequency', color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Set title and show legend
plt.title(f'Gaussian Distribution (n={num_samples})')
fig.legend(loc="upper right")

# Save the figure
plt.savefig(f'Figure_{num_samples}_Gaussian.png')

# Show the plot
plt.show()