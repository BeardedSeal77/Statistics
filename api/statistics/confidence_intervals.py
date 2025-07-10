# api/statistics/confidence_intervals.py
import numpy as np
from scipy import stats
from typing import Dict, Any, Optional
import math

class ConfidenceIntervals:
    """
    A comprehensive class for confidence interval calculations
    with detailed step-by-step explanations and formulas.
    """
    
    def __init__(self):
        """Initialize confidence interval calculator"""
        pass
    
    def mean_confidence_interval(self, 
                                sample_mean: float,
                                sample_size: int,
                                confidence_level: float,
                                population_std: Optional[float] = None,
                                sample_std: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate confidence interval for population mean
        
        Args:
            sample_mean: Sample mean (x̄)
            sample_size: Sample size (n)
            confidence_level: Confidence level (0-1, e.g., 0.95)
            population_std: Population standard deviation (σ) if known
            sample_std: Sample standard deviation (s) if population_std unknown
            
        Returns:
            Dictionary with confidence interval, steps, and interpretation
        """
        alpha = 1 - confidence_level
        alpha_half = alpha / 2
        
        # Determine whether to use z or t distribution
        if population_std is not None:
            # Use z-distribution (population std known)
            critical_value = stats.norm.ppf(1 - alpha_half)
            std_error = population_std / math.sqrt(sample_size)
            distribution_type = "z"
            df = None
            
            steps = [
                f"Given: x̄ = {sample_mean}, n = {sample_size}, σ = {population_std}",
                f"Confidence level = {confidence_level * 100}%",
                f"Step 1: Calculate α = 1 - {confidence_level} = {alpha}",
                f"Step 2: Find α/2 = {alpha}/2 = {alpha_half}",
                f"Step 3: Since σ is known, use z-distribution",
                f"z_{1-alpha_half} = {critical_value}",
                f"Step 4: Calculate standard error",
                f"SE = σ/√n = {population_std}/√{sample_size} = {std_error}",
                f"Step 5: Calculate margin of error",
                f"ME = z × SE = {critical_value} × {std_error} = {critical_value * std_error}",
                f"Step 6: Calculate confidence interval",
                f"CI = x̄ ± ME = {sample_mean} ± {critical_value * std_error}"
            ]
            
        else:
            # Use t-distribution (population std unknown)
            if sample_std is None:
                raise ValueError("Either population_std or sample_std must be provided")
            
            df = sample_size - 1
            critical_value = stats.t.ppf(1 - alpha_half, df)
            std_error = sample_std / math.sqrt(sample_size)
            distribution_type = "t"
            
            steps = [
                f"Given: x̄ = {sample_mean}, n = {sample_size}, s = {sample_std}",
                f"Confidence level = {confidence_level * 100}%",
                f"Step 1: Calculate α = 1 - {confidence_level} = {alpha}",
                f"Step 2: Find α/2 = {alpha}/2 = {alpha_half}",
                f"Step 3: Since σ is unknown, use t-distribution",
                f"Degrees of freedom = n - 1 = {sample_size} - 1 = {df}",
                f"t_{1-alpha_half},{df} = {critical_value}",
                f"Step 4: Calculate standard error",
                f"SE = s/√n = {sample_std}/√{sample_size} = {std_error}",
                f"Step 5: Calculate margin of error",
                f"ME = t × SE = {critical_value} × {std_error} = {critical_value * std_error}",
                f"Step 6: Calculate confidence interval",
                f"CI = x̄ ± ME = {sample_mean} ± {critical_value * std_error}"
            ]
        
        margin_error = critical_value * std_error
        lower_bound = sample_mean - margin_error
        upper_bound = sample_mean + margin_error
        
        # Add final bounds to steps
        steps.append(f"CI = [{lower_bound}, {upper_bound}]")
        
        return {
            'confidence_interval': [lower_bound, upper_bound],
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'margin_of_error': margin_error,
            'critical_value': critical_value,
            'standard_error': std_error,
            'distribution_type': distribution_type,
            'degrees_of_freedom': df,
            'confidence_level': confidence_level,
            'formula': f'CI = x̄ ± {distribution_type}_(α/2) × (σ/√n)' if distribution_type == 'z' else f'CI = x̄ ± t_(α/2,df) × (s/√n)',
            'steps': steps,
            'interpretation': f"We are {confidence_level * 100}% confident that the true population mean is between {lower_bound} and {upper_bound}",
            'description': f'{confidence_level * 100}% confidence interval for population mean'
        }
    
    def proportion_confidence_interval(self,
                                     sample_proportion: float,
                                     sample_size: int,
                                     confidence_level: float) -> Dict[str, Any]:
        """
        Calculate confidence interval for population proportion
        
        Args:
            sample_proportion: Sample proportion (p̂)
            sample_size: Sample size (n)
            confidence_level: Confidence level (0-1, e.g., 0.95)
            
        Returns:
            Dictionary with confidence interval, steps, and interpretation
        """
        alpha = 1 - confidence_level
        alpha_half = alpha / 2
        
        # Check normal approximation conditions
        np_hat = sample_size * sample_proportion
        nq_hat = sample_size * (1 - sample_proportion)
        
        if np_hat < 5 or nq_hat < 5:
            warning = f"Warning: Normal approximation may not be appropriate (np̂ = {np_hat}, nq̂ = {nq_hat}). Both should be ≥ 5."
        else:
            warning = None
        
        # Calculate confidence interval
        z_critical = stats.norm.ppf(1 - alpha_half)
        std_error = math.sqrt(sample_proportion * (1 - sample_proportion) / sample_size)
        margin_error = z_critical * std_error
        
        lower_bound = sample_proportion - margin_error
        upper_bound = sample_proportion + margin_error
        
        # Ensure bounds are within [0, 1]
        lower_bound = max(0, lower_bound)
        upper_bound = min(1, upper_bound)
        
        steps = [
            f"Given: p̂ = {sample_proportion}, n = {sample_size}",
            f"Confidence level = {confidence_level * 100}%",
            f"Step 1: Check normal approximation conditions",
            f"np̂ = {sample_size} × {sample_proportion} = {np_hat}",
            f"nq̂ = n(1-p̂) = {sample_size} × {1 - sample_proportion} = {nq_hat}",
            f"Both np̂ ≥ 5 and nq̂ ≥ 5? {'Yes' if np_hat >= 5 and nq_hat >= 5 else 'No'}",
            f"Step 2: Calculate α = 1 - {confidence_level} = {alpha}",
            f"Step 3: Find critical value z_{1-alpha_half} = {z_critical}",
            f"Step 4: Calculate standard error",
            f"SE = √[p̂(1-p̂)/n] = √[{sample_proportion} × {1-sample_proportion} / {sample_size}] = {std_error}",
            f"Step 5: Calculate margin of error",
            f"ME = z × SE = {z_critical} × {std_error} = {margin_error}",
            f"Step 6: Calculate confidence interval",
            f"CI = p̂ ± ME = {sample_proportion} ± {margin_error}",
            f"CI = [{lower_bound}, {upper_bound}]"
        ]
        
        return {
            'confidence_interval': [lower_bound, upper_bound],
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'margin_of_error': margin_error,
            'critical_value': z_critical,
            'standard_error': std_error,
            'confidence_level': confidence_level,
            'sample_proportion': sample_proportion,
            'sample_size': sample_size,
            'formula': 'CI = p̂ ± z_(α/2) × √[p̂(1-p̂)/n]',
            'steps': steps,
            'interpretation': f"We are {confidence_level * 100}% confident that the true population proportion is between {lower_bound:.4f} and {upper_bound:.4f}",
            'percentage_interpretation': f"We are {confidence_level * 100}% confident that the true population proportion is between {lower_bound * 100:.2f}% and {upper_bound * 100:.2f}%",
            'description': f'{confidence_level * 100}% confidence interval for population proportion',
            'warning': warning
        }
    
    def sample_size_for_mean(self,
                           margin_error: float,
                           confidence_level: float,
                           population_std: float) -> Dict[str, Any]:
        """
        Calculate required sample size for estimating population mean
        
        Args:
            margin_error: Desired margin of error
            confidence_level: Confidence level (0-1)
            population_std: Population standard deviation
            
        Returns:
            Dictionary with sample size calculation and steps
        """
        alpha = 1 - confidence_level
        z_critical = stats.norm.ppf(1 - alpha/2)
        
        # Calculate sample size
        n_exact = (z_critical * population_std / margin_error) ** 2
        n_required = math.ceil(n_exact)
        
        steps = [
            f"Given: ME = {margin_error}, confidence level = {confidence_level * 100}%, σ = {population_std}",
            f"Step 1: Find critical value z_{1-alpha/2} = {z_critical}",
            f"Step 2: Use sample size formula",
            f"n = (z × σ / ME)²",
            f"n = ({z_critical} × {population_std} / {margin_error})²",
            f"n = ({z_critical * population_std / margin_error})²",
            f"n = {n_exact}",
            f"Step 3: Round up to next integer",
            f"Required sample size = {n_required}"
        ]
        
        return {
            'sample_size_exact': n_exact,
            'sample_size_required': n_required,
            'margin_error': margin_error,
            'confidence_level': confidence_level,
            'critical_value': z_critical,
            'population_std': population_std,
            'formula': 'n = (z_(α/2) × σ / ME)²',
            'steps': steps,
            'description': f'Sample size needed for {confidence_level * 100}% confidence with margin of error {margin_error}'
        }
    
    def sample_size_for_proportion(self,
                                 margin_error: float,
                                 confidence_level: float,
                                 estimated_proportion: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate required sample size for estimating population proportion
        
        Args:
            margin_error: Desired margin of error
            confidence_level: Confidence level (0-1)
            estimated_proportion: Prior estimate of proportion (if None, uses 0.5 for maximum)
            
        Returns:
            Dictionary with sample size calculation and steps
        """
        alpha = 1 - confidence_level
        z_critical = stats.norm.ppf(1 - alpha/2)
        
        if estimated_proportion is None:
            # Use 0.5 for maximum sample size (most conservative)
            p_estimate = 0.5
            conservative = True
        else:
            p_estimate = estimated_proportion
            conservative = False
        
        # Calculate sample size
        n_exact = (z_critical ** 2 * p_estimate * (1 - p_estimate)) / (margin_error ** 2)
        n_required = math.ceil(n_exact)
        
        steps = [
            f"Given: ME = {margin_error}, confidence level = {confidence_level * 100}%",
            f"Prior estimate: p̂ = {p_estimate} {'(conservative estimate)' if conservative else ''}",
            f"Step 1: Find critical value z_{1-alpha/2} = {z_critical}",
            f"Step 2: Use sample size formula",
            f"n = z² × p̂(1-p̂) / ME²",
            f"n = {z_critical}² × {p_estimate} × {1-p_estimate} / {margin_error}²",
            f"n = {z_critical**2} × {p_estimate * (1-p_estimate)} / {margin_error**2}",
            f"n = {n_exact}",
            f"Step 3: Round up to next integer",
            f"Required sample size = {n_required}"
        ]
        
        return {
            'sample_size_exact': n_exact,
            'sample_size_required': n_required,
            'margin_error': margin_error,
            'confidence_level': confidence_level,
            'critical_value': z_critical,
            'estimated_proportion': p_estimate,
            'conservative_estimate': conservative,
            'formula': 'n = z²_(α/2) × p̂(1-p̂) / ME²',
            'steps': steps,
            'description': f'Sample size needed for {confidence_level * 100}% confidence with margin of error {margin_error}'
        }