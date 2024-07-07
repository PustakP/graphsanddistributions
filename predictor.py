import numpy as np
import matplotlib.pyplot as plt
from both import poisson_distribution
from scipy.optimize import minimize_scalar
import math
import random

# Poisson PMF function
def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

# Function to calculate the mean squared error
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Function to find the optimal lambda using minimize_scalar
def find_optimal_lambda(partial_data):
    def objective(lam):
        pred = [poisson_pmf(k, lam) for k in range(len(partial_data))]
        return mse(partial_data, pred)
    
    result = minimize_scalar(objective, bounds=(0, 20), method='bounded')
    return result.x

# Gradient descent function to refine lambda
def gradient_descent(partial_data, initial_lambda, learning_rate, num_iterations):
    lam = initial_lambda
    for _ in range(num_iterations):
        pred = [poisson_pmf(k, lam) for k in range(len(partial_data))]
        gradient = -2 * sum((partial_data[k] - pred[k]) * k * pred[k] / lam for k in range(len(partial_data)))
        lam -= learning_rate * gradient
    return max(0, lam)  # Ensure lambda is non-negative

# Main function
def main():
    # Generate full Poisson distribution
    true_lambda = random.randint( 1,10)
    num_samples = 1000
    full_samples = poisson_distribution(true_lambda, num_samples)
    
    # Create histogram of full samples
    full_hist, bins = np.histogram(full_samples, bins=range(max(full_samples) + 2), density=True)
    
    # Generate partial data (first half of the distribution)
    partial_data = full_hist[:len(full_hist) // 2]
    
    # Find optimal lambda using minimize_scalar
    optimal_lambda = find_optimal_lambda(partial_data)
    
    # Refine lambda using gradient descent
    refined_lambda = gradient_descent(partial_data, optimal_lambda, learning_rate=0.01, num_iterations=100)
    
    # Generate predicted distribution using refined lambda
    x = np.arange(len(full_hist))
    predicted_dist = [poisson_pmf(k, refined_lambda) for k in range(len(full_hist))]
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot true distribution and partial data
    ax1.bar(x, full_hist, alpha=0.5, label='True Distribution')
    ax1.plot(x, full_hist, 'r-', label=f'True Distribution Line (λ={refined_lambda:.2f})')
    ax1.bar(x[:len(partial_data)], partial_data, alpha=0.7, label='Partial Data')
    ax1.axvline(x=len(partial_data) - 0.5, color='r', linestyle='--', label='Partial Data Cutoff')
    ax1.set_title(f'True Poisson Distribution (λ={true_lambda})')
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Probability')
    ax1.legend()
    
    # Plot predicted distribution
    ax2.bar(x, full_hist, alpha=0.5, label='True Distribution')
    ax2.plot(x, predicted_dist, 'r-', label=f'Predicted Distribution (λ={refined_lambda:.2f})')
    ax2.axvline(x=len(partial_data) - 0.5, color='g', linestyle='--', label='Partial Data Cutoff')
    ax2.set_title(f'Predicted Poisson Distribution (λ={refined_lambda:.2f})')
    ax2.set_xlabel('Value')
    ax2.set_ylabel('Probability')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f'poisson_prediction_comparison_Lambda-{true_lambda}.png')
    plt.show()
    
    print(f"True lambda: {true_lambda}")
    print(f"Optimal lambda: {optimal_lambda:.2f}")
    print(f"Refined lambda: {refined_lambda:.2f}")

main()