import random
import math
import matplotlib.pyplot as plt

def gaussian_distribution(mean, std_dev, num_samples):
    samples = []
    for _ in range(num_samples // 2):
        u1, u2 = random.random(), random.random()
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        x1, x2 = z1 * std_dev + mean, z2 * std_dev + mean
        samples.extend([x1, x2])
    return samples[:num_samples]


def poisson_distribution(lam, num_samples):
    samples = []
    for _ in range(num_samples):
        L = math.exp(-lam)  # Directly using the exponential function for e^-λ
        k = 0
        p = 1.0

        while p > L:
            k += 1
            p *= random.random()

        samples.append(k - 1)  # Subtracting one because the loop increments k one time too many

    return samples

def plot_distribution(samples, dist_type, num_samples, param, bins=35):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Probability Density', color='g')
    ax1.tick_params(axis='y', labelcolor='g')

    n, bins, patches = ax1.hist(samples, bins=bins, density=True, alpha=0.6, color='g', label='Histogram')

    midpoints = (bins[:-1] + bins[1:]) / 2
    convolution = n

    ax2 = ax1.twinx()
    ax2.plot(midpoints, convolution, color='b', label='Midpoint Line', linewidth=2)
    ax2.set_ylabel('Frequency', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    if dist_type == 'Gaussian':
        plt.title(f'Gaussian Distribution (n={num_samples}, μ={param[0]}, σ={param[1]})')
    elif dist_type == 'Poisson':
        plt.title(f'Poisson Distribution (n={num_samples}, λ={param})')
        file_dist_type = 'Poisson_Lambda_{}'.format(int(param))
        
        # Overlay Poisson distribution using the direct formula
        poisson_values = [((param ** k) * math.exp(-param)) / math.factorial(k) for k in range(int(max(samples)) + 1)]
        ax2.plot(range(len(poisson_values)), poisson_values, 'r--', label='Poisson Formula', linewidth=2)

    fig.legend(loc="upper right")
    plt.savefig(f'Figure_{num_samples}_{file_dist_type if dist_type == "Poisson" else dist_type}.png')
    plt.show()
'''
gradient
simplex


'''
def main():
    dist_type = input("Enter distribution type (Gaussian/Poisson): ").strip().lower()
    num_samples = int(input("Enter the number of samples: ")) # number of samples to generate
    
    if dist_type == 'gaussian':
        mean = float(input("Enter mean: "))
        std_dev = float(input("Enter standard deviation: "))
        samples = gaussian_distribution(mean, std_dev, num_samples)
        plot_distribution(samples, 'Gaussian', num_samples, (mean, std_dev))
    elif dist_type == 'poisson':
        lam = float(input("Enter lambda (average rate): "))
        samples = poisson_distribution(lam, num_samples)
        plot_distribution(samples, 'Poisson', num_samples, lam, bins=35)
    else:
        print("Invalid distribution type.")

if __name__ == "__main__":
    main()