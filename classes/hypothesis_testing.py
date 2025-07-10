# api/statistics/normal_distribution.py
import numpy as np
from scipy import stats
from typing import Dict, Any, Optional
import math

class NormalDistribution:
    """
    A comprehensive class for normal distribution calculations
    with detailed step-by-step explanations and formulas.
    """
    
    def __init__(self, mean: float, std_dev: float):
        """
        Initialize normal distribution
        
        Args:
            mean: Population mean (μ)
            std_dev: Population standard deviation (σ)
        """
        self.mean = mean
        self.std_dev = std_dev
        
    def calculate_z_score(self, x_value: float) -> Dict[str, Any]:
        """
        Calculate z-score for a given value
        
        Args:
            x_value: The value to calculate z-score for
            
        Returns:
            Dictionary with z-score, steps, and interpretation
        """
        z_score = (x_value - self.mean) / self.std_dev
        
        steps = [
            f"Given: μ = {self.mean}, σ = {self.std_dev}, x = {x_value}",
            f"Z = (x - μ) / σ",
            f"Z = ({x_value} - {self.mean}) / {self.std_dev}",
            f"Z = {x_value - self.mean} / {self.std_dev}",
            f"Z = {z_score}"
        ]
        
        # Interpretation
        if abs(z_score) < 1:
            interpretation = "Within 1 standard deviation of the mean (common)"
        elif abs(z_score) < 2:
            interpretation = "Within 2 standard deviations of the mean (fairly common)"
        elif abs(z_score) < 3:
            interpretation = "Within 3 standard deviations of the mean (uncommon)"
        else:
            interpretation = "More than 3 standard deviations from the mean (very rare)"
        
        return {
            'z_score': z_score,
            'formula': 'Z = (x - μ) / σ',
            'steps': steps,
            'interpretation': interpretation,
            'description': 'Standardized score showing how many standard deviations from the mean'
        }
    
    def calculate_probability(self, x_value: float, comparison: str = 'less_than') -> Dict[str, Any]:
        """
        Calculate probability for normal distribution
        
        Args:
            x_value: The value to calculate probability for
            comparison: 'less_than', 'greater_than', or 'equal_to'
            
        Returns:
            Dictionary with probability, steps, and visualization info
        """
        z_score = (x_value - self.mean) / self.std_dev
        
        if comparison == 'less_than':
            probability = stats.norm.cdf(z_score)
            prob_description = f"P(X < {x_value})"
        elif comparison == 'greater_than':
            probability = 1 - stats.norm.cdf(z_score)
            prob_description = f"P(X > {x_value})"
        else:  # between values would be handled differently
            probability = stats.norm.cdf(z_score)
            prob_description = f"P(X ≤ {x_value})"
        
        steps = [
            f"Given: μ = {self.mean}, σ = {self.std_dev}, x = {x_value}",
            f"Step 1: Calculate z-score",
            f"Z = (x - μ) / σ = ({x_value} - {self.mean}) / {self.std_dev} = {z_score}",
            f"Step 2: Find probability using standard normal table",
            f"{prob_description} = P(Z < {z_score}) = {probability}" if comparison == 'less_than' 
            else f"{prob_description} = 1 - P(Z < {z_score}) = 1 - {stats.norm.cdf(z_score)} = {probability}"
        ]
        
        return {
            'probability': probability,
            'z_score': z_score,
            'formula': 'P = Φ(z) where Φ is the standard normal CDF',
            'steps': steps,
            'description': f'Probability that X {comparison.replace("_", " ")} {x_value}',
            'percentage': probability * 100
        }
    
    def calculate_probability_between(self, x1: float, x2: float) -> Dict[str, Any]:
        """
        Calculate probability between two values
        
        Args:
            x1: Lower bound
            x2: Upper bound
            
        Returns:
            Dictionary with probability, steps, and visualization info
        """
        # Ensure x1 < x2
        if x1 > x2:
            x1, x2 = x2, x1
        
        z1 = (x1 - self.mean) / self.std_dev
        z2 = (x2 - self.mean) / self.std_dev
        
        prob_z1 = stats.norm.cdf(z1)
        prob_z2 = stats.norm.cdf(z2)
        probability = prob_z2 - prob_z1
        
        steps = [
            f"Given: μ = {self.mean}, σ = {self.std_dev}",
            f"Find P({x1} < X < {x2})",
            f"Step 1: Calculate z-scores",
            f"Z₁ = ({x1} - {self.mean}) / {self.std_dev} = {z1}",
            f"Z₂ = ({x2} - {self.mean}) / {self.std_dev} = {z2}",
            f"Step 2: Find probabilities",
            f"P(Z < {z1}) = {prob_z1}",
            f"P(Z < {z2}) = {prob_z2}",
            f"Step 3: Calculate difference",
            f"P({x1} < X < {x2}) = P(Z < {z2}) - P(Z < {z1})",
            f"P({x1} < X < {x2}) = {prob_z2} - {prob_z1} = {probability}"
        ]
        
        return {
            'probability': probability,
            'z_scores': [z1, z2],
            'formula': 'P(a < X < b) = Φ(z₂) - Φ(z₁)',
            'steps': steps,
            'description': f'Probability that X is between {x1} and {x2}',
            'percentage': probability * 100
        }
    
    def find_percentile(self, percentile: float) -> Dict[str, Any]:
        """
        Find the value at a given percentile
        
        Args:
            percentile: Percentile (0-100)
            
        Returns:
            Dictionary with x-value, steps, and interpretation
        """
        # Convert percentile to proportion
        p = percentile / 100
        
        # Find z-score for this percentile
        z_score = stats.norm.ppf(p)
        
        # Convert back to x-value
        x_value = self.mean + z_score * self.std_dev
        
        steps = [
            f"Given: μ = {self.mean}, σ = {self.std_dev}",
            f"Find the {percentile}th percentile",
            f"Step 1: Convert percentile to proportion: p = {percentile}/100 = {p}",
            f"Step 2: Find z-score where P(Z < z) = {p}",
            f"From standard normal table: z = {z_score}",
            f"Step 3: Convert z-score to x-value",
            f"x = μ + z × σ = {self.mean} + {z_score} × {self.std_dev}",
            f"x = {self.mean} + {z_score * self.std_dev} = {x_value}"
        ]
        
        return {
            'x_value': x_value,
            'z_score': z_score,
            'percentile': percentile,
            'formula': 'x = μ + z × σ',
            'steps': steps,
            'description': f'{percentile}% of values fall below {x_value}',
            'interpretation': f'The {percentile}th percentile is {x_value}'
        }
    
    def find_critical_values(self, confidence_level: float) -> Dict[str, Any]:
        """
        Find critical values for confidence interval
        
        Args:
            confidence_level: Confidence level (0-1, e.g., 0.95 for 95%)
            
        Returns:
            Dictionary with critical values and steps
        """
        alpha = 1 - confidence_level
        alpha_half = alpha / 2
        
        # Find z-critical values
        z_lower = stats.norm.ppf(alpha_half)
        z_upper = stats.norm.ppf(1 - alpha_half)
        
        # Convert to x-values
        x_lower = self.mean + z_lower * self.std_dev
        x_upper = self.mean + z_upper * self.std_dev
        
        steps = [
            f"Given: μ = {self.mean}, σ = {self.std_dev}",
            f"Confidence level = {confidence_level * 100}%",
            f"Step 1: Calculate α = 1 - {confidence_level} = {alpha}",
            f"Step 2: Find α/2 = {alpha}/2 = {alpha_half}",
            f"Step 3: Find critical z-values",
            f"z_lower = z_{alpha_half} = {z_lower}",
            f"z_upper = z_{1 - alpha_half} = {z_upper}",
            f"Step 4: Convert to x-values",
            f"x_lower = μ + z_lower × σ = {self.mean} + {z_lower} × {self.std_dev} = {x_lower}",
            f"x_upper = μ + z_upper × σ = {self.mean} + {z_upper} × {self.std_dev} = {x_upper}"
        ]
        
        return {
            'z_critical_lower': z_lower,
            'z_critical_upper': z_upper,
            'x_critical_lower': x_lower,
            'x_critical_upper': x_upper,
            'confidence_level': confidence_level,
            'formula': 'x = μ ± z_(α/2) × σ',
            'steps': steps,
            'description': f'Critical values for {confidence_level * 100}% confidence interval'
        }
    
    def empirical_rule(self) -> Dict[str, Any]:
        """
        Calculate empirical rule (68-95-99.7 rule) boundaries
        
        Returns:
            Dictionary with boundaries and percentages
        """
        # 68% (±1 standard deviation)
        one_std_lower = self.mean - self.std_dev
        one_std_upper = self.mean + self.std_dev
        
        # 95% (±2 standard deviations)
        two_std_lower = self.mean - 2 * self.std_dev
        two_std_upper = self.mean + 2 * self.std_dev
        
        # 99.7% (±3 standard deviations)
        three_std_lower = self.mean - 3 * self.std_dev
        three_std_upper = self.mean + 3 * self.std_dev
        
        steps = [
            f"Given: μ = {self.mean}, σ = {self.std_dev}",
            f"Empirical Rule (68-95-99.7 Rule):",
            f"68% of data falls within μ ± 1σ = {self.mean} ± {self.std_dev} = [{one_std_lower}, {one_std_upper}]",
            f"95% of data falls within μ ± 2σ = {self.mean} ± {2 * self.std_dev} = [{two_std_lower}, {two_std_upper}]",
            f"99.7% of data falls within μ ± 3σ = {self.mean} ± {3 * self.std_dev} = [{three_std_lower}, {three_std_upper}]"
        ]
        
        return {
            'one_std': {
                'lower': one_std_lower,
                'upper': one_std_upper,
                'percentage': 68,
                'description': '68% of data falls within 1 standard deviation'
            },
            'two_std': {
                'lower': two_std_lower,
                'upper': two_std_upper,
                'percentage': 95,
                'description': '95% of data falls within 2 standard deviations'
            },
            'three_std': {
                'lower': three_std_lower,
                'upper': three_std_upper,
                'percentage': 99.7,
                'description': '99.7% of data falls within 3 standard deviations'
            },
            'formula': 'μ ± kσ where k = 1, 2, or 3',
            'steps': steps,
            'description': 'Empirical rule boundaries for normal distribution'
        }