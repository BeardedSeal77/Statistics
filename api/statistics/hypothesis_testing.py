# api/statistics/hypothesis_testing.py
import numpy as np
from scipy import stats
from typing import Dict, Any, Optional, Literal
import math

class HypothesisTesting:
    """
    A comprehensive class for hypothesis testing calculations
    with detailed step-by-step explanations and formulas.
    """
    
    def __init__(self):
        """Initialize hypothesis testing calculator"""
        pass
    
    def one_sample_mean_test(self,
                           sample_mean: float,
                           sample_size: int,
                           null_mean: float,
                           alpha: float,
                           test_type: Literal['two-tailed', 'left-tailed', 'right-tailed'],
                           population_std: Optional[float] = None,
                           sample_std: Optional[float] = None) -> Dict[str, Any]:
        """
        Perform one-sample mean hypothesis test
        
        Args:
            sample_mean: Sample mean (x̄)
            sample_size: Sample size (n)
            null_mean: Hypothesized population mean (μ₀)
            alpha: Significance level (α)
            test_type: Type of test
            population_std: Population standard deviation (σ) if known
            sample_std: Sample standard deviation (s) if population_std unknown
            
        Returns:
            Dictionary with test results, steps, and interpretation
        """
        
        # Set up hypotheses
        if test_type == 'two-tailed':
            h0 = f"H₀: μ = {null_mean}"
            h1 = f"H₁: μ ≠ {null_mean}"
        elif test_type == 'left-tailed':
            h0 = f"H₀: μ = {null_mean}"
            h1 = f"H₁: μ < {null_mean}"
        else:  # right-tailed
            h0 = f"H₀: μ = {null_mean}"
            h1 = f"H₁: μ > {null_mean}"
        
        # Determine test statistic and distribution
        if population_std is not None:
            # Z-test (population std known)
            std_error = population_std / math.sqrt(sample_size)
            test_stat = (sample_mean - null_mean) / std_error
            distribution_type = "z"
            df = None
            
            # Critical values and p-value
            if test_type == 'two-tailed':
                critical_values = [-stats.norm.ppf(1 - alpha/2), stats.norm.ppf(1 - alpha/2)]
                p_value = 2 * (1 - stats.norm.cdf(abs(test_stat)))
            elif test_type == 'left-tailed':
                critical_values = [stats.norm.ppf(alpha)]
                p_value = stats.norm.cdf(test_stat)
            else:  # right-tailed
                critical_values = [stats.norm.ppf(1 - alpha)]
                p_value = 1 - stats.norm.cdf(test_stat)
                
        else:
            # T-test (population std unknown)
            if sample_std is None:
                raise ValueError("Either population_std or sample_std must be provided")
            
            df = sample_size - 1
            std_error = sample_std / math.sqrt(sample_size)
            test_stat = (sample_mean - null_mean) / std_error
            distribution_type = "t"
            
            # Critical values and p-value
            if test_type == 'two-tailed':
                critical_values = [-stats.t.ppf(1 - alpha/2, df), stats.t.ppf(1 - alpha/2, df)]
                p_value = 2 * (1 - stats.t.cdf(abs(test_stat), df))
            elif test_type == 'left-tailed':
                critical_values = [stats.t.ppf(alpha, df)]
                p_value = stats.t.cdf(test_stat, df)
            else:  # right-tailed
                critical_values = [stats.t.ppf(1 - alpha, df)]
                p_value = 1 - stats.t.cdf(test_stat, df)
        
        # Decision
        if test_type == 'two-tailed':
            reject_null = abs(test_stat) > abs(critical_values[1])
        elif test_type == 'left-tailed':
            reject_null = test_stat < critical_values[0]
        else:  # right-tailed
            reject_null = test_stat > critical_values[0]
        
        # Build steps
        steps = [
            f"Step 1: State the hypotheses",
            f"{h0}",
            f"{h1}",
            f"Step 2: Set significance level α = {alpha}",
            f"Step 3: Choose test statistic",
            f"Using {'z-test' if distribution_type == 'z' else 't-test'} ({'σ known' if population_std else 'σ unknown'})",
            f"Step 4: Calculate test statistic",
            f"Given: x̄ = {sample_mean}, μ₀ = {null_mean}, n = {sample_size}",
        ]
        
        if population_std is not None:
            steps.extend([
                f"σ = {population_std}",
                f"SE = σ/√n = {population_std}/√{sample_size} = {std_error}",
                f"z = (x̄ - μ₀)/SE = ({sample_mean} - {null_mean})/{std_error} = {test_stat}"
            ])
        else:
            steps.extend([
                f"s = {sample_std}",
                f"df = n - 1 = {sample_size} - 1 = {df}",
                f"SE = s/√n = {sample_std}/√{sample_size} = {std_error}",
                f"t = (x̄ - μ₀)/SE = ({sample_mean} - {null_mean})/{std_error} = {test_stat}"
            ])
        
        steps.extend([
            f"Step 5: Find critical value(s) and p-value",
            f"Critical value(s): {critical_values}",
            f"p-value = {p_value}",
            f"Step 6: Make decision",
            f"Since p-value ({p_value}) {'<' if reject_null else '≥'} α ({alpha}), we {'reject' if reject_null else 'fail to reject'} H₀"
        ])
        
        return {
            'test_statistic': test_stat,
            'critical_values': critical_values,
            'p_value': p_value,
            'alpha': alpha,
            'reject_null': reject_null,
            'distribution_type': distribution_type,
            'degrees_of_freedom': df,
            'standard_error': std_error,
            'test_type': test_type,
            'null_hypothesis': h0,
            'alternative_hypothesis': h1,
            'formula': f'{distribution_type} = (x̄ - μ₀) / ({"σ" if population_std else "s"}/√n)',
            'steps': steps,
            'conclusion': f"{'Reject' if reject_null else 'Fail to reject'} the null hypothesis at α = {alpha} level",
            'interpretation': f"There {'is' if reject_null else 'is not'} sufficient evidence to conclude that the population proportion {'is not equal to' if test_type == 'two-tailed' else 'is less than' if test_type == 'left-tailed' else 'is greater than'} {null_proportion}",
            'description': 'One-sample z-test for population proportion',
            'warning': warning
        }
    
    def two_sample_mean_test(self,
                           sample1_mean: float,
                           sample1_size: int,
                           sample1_std: float,
                           sample2_mean: float,
                           sample2_size: int,
                           sample2_std: float,
                           alpha: float,
                           test_type: Literal['two-tailed', 'left-tailed', 'right-tailed'],
                           equal_variances: bool = True) -> Dict[str, Any]:
        """
        Perform two-sample mean hypothesis test
        
        Args:
            sample1_mean: Sample 1 mean (x̄₁)
            sample1_size: Sample 1 size (n₁)
            sample1_std: Sample 1 standard deviation (s₁)
            sample2_mean: Sample 2 mean (x̄₂)
            sample2_size: Sample 2 size (n₂)
            sample2_std: Sample 2 standard deviation (s₂)
            alpha: Significance level (α)
            test_type: Type of test
            equal_variances: Whether to assume equal variances
            
        Returns:
            Dictionary with test results, steps, and interpretation
        """
        
        # Set up hypotheses
        if test_type == 'two-tailed':
            h0 = "H₀: μ₁ = μ₂ (or μ₁ - μ₂ = 0)"
            h1 = "H₁: μ₁ ≠ μ₂ (or μ₁ - μ₂ ≠ 0)"
        elif test_type == 'left-tailed':
            h0 = "H₀: μ₁ = μ₂ (or μ₁ - μ₂ = 0)"
            h1 = "H₁: μ₁ < μ₂ (or μ₁ - μ₂ < 0)"
        else:  # right-tailed
            h0 = "H₀: μ₁ = μ₂ (or μ₁ - μ₂ = 0)"
            h1 = "H₁: μ₁ > μ₂ (or μ₁ - μ₂ > 0)"
        
        if equal_variances:
            # Pooled variance t-test
            pooled_var = ((sample1_size - 1) * sample1_std**2 + (sample2_size - 1) * sample2_std**2) / (sample1_size + sample2_size - 2)
            pooled_std = math.sqrt(pooled_var)
            std_error = pooled_std * math.sqrt(1/sample1_size + 1/sample2_size)
            df = sample1_size + sample2_size - 2
            
            variance_steps = [
                f"Pooled variance: s²ₚ = [(n₁-1)s₁² + (n₂-1)s₂²] / (n₁+n₂-2)",
                f"s²ₚ = [({sample1_size}-1)×{sample1_std}² + ({sample2_size}-1)×{sample2_std}²] / ({sample1_size}+{sample2_size}-2)",
                f"s²ₚ = [{sample1_size-1}×{sample1_std**2} + {sample2_size-1}×{sample2_std**2}] / {sample1_size + sample2_size - 2}",
                f"s²ₚ = {pooled_var}",
                f"sₚ = √{pooled_var} = {pooled_std}",
                f"SE = sₚ√(1/n₁ + 1/n₂) = {pooled_std}√(1/{sample1_size} + 1/{sample2_size}) = {std_error}"
            ]
        else:
            # Welch's t-test (unequal variances)
            std_error = math.sqrt(sample1_std**2/sample1_size + sample2_std**2/sample2_size)
            # Welch-Satterthwaite equation for degrees of freedom
            numerator = (sample1_std**2/sample1_size + sample2_std**2/sample2_size)**2
            denominator = (sample1_std**2/sample1_size)**2/(sample1_size-1) + (sample2_std**2/sample2_size)**2/(sample2_size-1)
            df = numerator / denominator
            
            variance_steps = [
                f"Welch's t-test (unequal variances assumed)",
                f"SE = √(s₁²/n₁ + s₂²/n₂) = √({sample1_std}²/{sample1_size} + {sample2_std}²/{sample2_size}) = {std_error}",
                f"df = (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1)] = {df}"
            ]
        
        # Calculate test statistic
        t_stat = (sample1_mean - sample2_mean) / std_error
        
        # Critical values and p-value
        if test_type == 'two-tailed':
            critical_values = [-stats.t.ppf(1 - alpha/2, df), stats.t.ppf(1 - alpha/2, df)]
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
        elif test_type == 'left-tailed':
            critical_values = [stats.t.ppf(alpha, df)]
            p_value = stats.t.cdf(t_stat, df)
        else:  # right-tailed
            critical_values = [stats.t.ppf(1 - alpha, df)]
            p_value = 1 - stats.t.cdf(t_stat, df)
        
        # Decision
        if test_type == 'two-tailed':
            reject_null = abs(t_stat) > abs(critical_values[1])
        elif test_type == 'left-tailed':
            reject_null = t_stat < critical_values[0]
        else:  # right-tailed
            reject_null = t_stat > critical_values[0]
        
        steps = [
            f"Step 1: State the hypotheses",
            f"{h0}",
            f"{h1}",
            f"Step 2: Set significance level α = {alpha}",
            f"Step 3: Calculate test statistic",
            f"Given: x̄₁ = {sample1_mean}, n₁ = {sample1_size}, s₁ = {sample1_std}",
            f"       x̄₂ = {sample2_mean}, n₂ = {sample2_size}, s₂ = {sample2_std}",
            *variance_steps,
            f"t = (x̄₁ - x̄₂) / SE = ({sample1_mean} - {sample2_mean}) / {std_error} = {t_stat}",
            f"Step 4: Find critical value(s) and p-value",
            f"df = {df}",
            f"Critical value(s): {critical_values}",
            f"p-value = {p_value}",
            f"Step 5: Make decision",
            f"Since p-value ({p_value}) {'<' if reject_null else '≥'} α ({alpha}), we {'reject' if reject_null else 'fail to reject'} H₀"
        ]
        
        return {
            'test_statistic': t_stat,
            'critical_values': critical_values,
            'p_value': p_value,
            'alpha': alpha,
            'reject_null': reject_null,
            'degrees_of_freedom': df,
            'standard_error': std_error,
            'test_type': test_type,
            'equal_variances': equal_variances,
            'null_hypothesis': h0,
            'alternative_hypothesis': h1,
            'pooled_variance': pooled_var if equal_variances else None,
            'formula': 't = (x̄₁ - x̄₂) / SE',
            'steps': steps,
            'conclusion': f"{'Reject' if reject_null else 'Fail to reject'} the null hypothesis at α = {alpha} level",
            'interpretation': f"There {'is' if reject_null else 'is not'} sufficient evidence to conclude that there is a significant difference between the two population means",
            'description': f'Two-sample t-test for difference in means ({"equal" if equal_variances else "unequal"} variances)'
        }
    
    def two_sample_proportion_test(self,
                                 sample1_successes: int,
                                 sample1_size: int,
                                 sample2_successes: int,
                                 sample2_size: int,
                                 alpha: float,
                                 test_type: Literal['two-tailed', 'left-tailed', 'right-tailed']) -> Dict[str, Any]:
        """
        Perform two-sample proportion hypothesis test
        
        Args:
            sample1_successes: Number of successes in sample 1
            sample1_size: Sample 1 size (n₁)
            sample2_successes: Number of successes in sample 2
            sample2_size: Sample 2 size (n₂)
            alpha: Significance level (α)
            test_type: Type of test
            
        Returns:
            Dictionary with test results, steps, and interpretation
        """
        
        # Calculate sample proportions
        p1_hat = sample1_successes / sample1_size
        p2_hat = sample2_successes / sample2_size
        
        # Calculate pooled proportion
        p_pooled = (sample1_successes + sample2_successes) / (sample1_size + sample2_size)
        q_pooled = 1 - p_pooled
        
        # Check normal approximation conditions
        conditions = [
            sample1_size * p_pooled >= 5,
            sample1_size * q_pooled >= 5,
            sample2_size * p_pooled >= 5,
            sample2_size * q_pooled >= 5
        ]
        
        if not all(conditions):
            warning = f"Warning: Normal approximation conditions not met. All of n₁p̂, n₁q̂, n₂p̂, n₂q̂ should be ≥ 5."
        else:
            warning = None
        
        # Set up hypotheses
        if test_type == 'two-tailed':
            h0 = "H₀: p₁ = p₂ (or p₁ - p₂ = 0)"
            h1 = "H₁: p₁ ≠ p₂ (or p₁ - p₂ ≠ 0)"
        elif test_type == 'left-tailed':
            h0 = "H₀: p₁ = p₂ (or p₁ - p₂ = 0)"
            h1 = "H₁: p₁ < p₂ (or p₁ - p₂ < 0)"
        else:  # right-tailed
            h0 = "H₀: p₁ = p₂ (or p₁ - p₂ = 0)"
            h1 = "H₁: p₁ > p₂ (or p₁ - p₂ > 0)"
        
        # Calculate standard error
        std_error = math.sqrt(p_pooled * q_pooled * (1/sample1_size + 1/sample2_size))
        
        # Calculate test statistic
        z_stat = (p1_hat - p2_hat) / std_error
        
        # Critical values and p-value
        if test_type == 'two-tailed':
            critical_values = [-stats.norm.ppf(1 - alpha/2), stats.norm.ppf(1 - alpha/2)]
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        elif test_type == 'left-tailed':
            critical_values = [stats.norm.ppf(alpha)]
            p_value = stats.norm.cdf(z_stat)
        else:  # right-tailed
            critical_values = [stats.norm.ppf(1 - alpha)]
            p_value = 1 - stats.norm.cdf(z_stat)
        
        # Decision
        if test_type == 'two-tailed':
            reject_null = abs(z_stat) > abs(critical_values[1])
        elif test_type == 'left-tailed':
            reject_null = z_stat < critical_values[0]
        else:  # right-tailed
            reject_null = z_stat > critical_values[0]
        
        steps = [
            f"Step 1: State the hypotheses",
            f"{h0}",
            f"{h1}",
            f"Step 2: Calculate sample proportions",
            f"p̂₁ = {sample1_successes}/{sample1_size} = {p1_hat}",
            f"p̂₂ = {sample2_successes}/{sample2_size} = {p2_hat}",
            f"Step 3: Calculate pooled proportion",
            f"p̂ = (x₁ + x₂)/(n₁ + n₂) = ({sample1_successes} + {sample2_successes})/({sample1_size} + {sample2_size}) = {p_pooled}",
            f"Step 4: Check normal approximation conditions",
            f"n₁p̂ = {sample1_size} × {p_pooled} = {sample1_size * p_pooled}",
            f"n₁q̂ = {sample1_size} × {q_pooled} = {sample1_size * q_pooled}",
            f"n₂p̂ = {sample2_size} × {p_pooled} = {sample2_size * p_pooled}",
            f"n₂q̂ = {sample2_size} × {q_pooled} = {sample2_size * q_pooled}",
            f"All ≥ 5? {'Yes' if all(conditions) else 'No'}",
            f"Step 5: Set significance level α = {alpha}",
            f"Step 6: Calculate test statistic",
            f"SE = √[p̂q̂(1/n₁ + 1/n₂)] = √[{p_pooled} × {q_pooled} × (1/{sample1_size} + 1/{sample2_size})] = {std_error}",
            f"z = (p̂₁ - p̂₂) / SE = ({p1_hat} - {p2_hat}) / {std_error} = {z_stat}",
            f"Step 7: Find critical value(s) and p-value",
            f"Critical value(s): {critical_values}",
            f"p-value = {p_value}",
            f"Step 8: Make decision",
            f"Since p-value ({p_value}) {'<' if reject_null else '≥'} α ({alpha}), we {'reject' if reject_null else 'fail to reject'} H₀"
        ]
        
        return {
            'test_statistic': z_stat,
            'critical_values': critical_values,
            'p_value': p_value,
            'alpha': alpha,
            'reject_null': reject_null,
            'standard_error': std_error,
            'test_type': test_type,
            'sample1_proportion': p1_hat,
            'sample2_proportion': p2_hat,
            'pooled_proportion': p_pooled,
            'null_hypothesis': h0,
            'alternative_hypothesis': h1,
            'formula': 'z = (p̂₁ - p̂₂) / √[p̂q̂(1/n₁ + 1/n₂)]',
            'steps': steps,
            'conclusion': f"{'Reject' if reject_null else 'Fail to reject'} the null hypothesis at α = {alpha} level",
            'interpretation': f"There {'is' if reject_null else 'is not'} sufficient evidence to conclude that there is a significant difference between the two population proportions",
            'description': 'Two-sample z-test for difference in proportions',
            'warning': warning
        }is not'} sufficient evidence to conclude that the population mean {'is not equal to' if test_type == 'two-tailed' else 'is less than' if test_type == 'left-tailed' else 'is greater than'} {null_mean}",
            'description': f'One-sample {distribution_type}-test for population mean'
        }
    
    def one_sample_proportion_test(self,
                                 sample_proportion: float,
                                 sample_size: int,
                                 null_proportion: float,
                                 alpha: float,
                                 test_type: Literal['two-tailed', 'left-tailed', 'right-tailed']) -> Dict[str, Any]:
        """
        Perform one-sample proportion hypothesis test
        
        Args:
            sample_proportion: Sample proportion (p̂)
            sample_size: Sample size (n)
            null_proportion: Hypothesized population proportion (p₀)
            alpha: Significance level (α)
            test_type: Type of test
            
        Returns:
            Dictionary with test results, steps, and interpretation
        """
        
        # Check normal approximation conditions
        np0 = sample_size * null_proportion
        nq0 = sample_size * (1 - null_proportion)
        
        if np0 < 5 or nq0 < 5:
            warning = f"Warning: Normal approximation may not be appropriate (np₀ = {np0}, nq₀ = {nq0}). Both should be ≥ 5."
        else:
            warning = None
        
        # Set up hypotheses
        if test_type == 'two-tailed':
            h0 = f"H₀: p = {null_proportion}"
            h1 = f"H₁: p ≠ {null_proportion}"
        elif test_type == 'left-tailed':
            h0 = f"H₀: p = {null_proportion}"
            h1 = f"H₁: p < {null_proportion}"
        else:  # right-tailed
            h0 = f"H₀: p = {null_proportion}"
            h1 = f"H₁: p > {null_proportion}"
        
        # Calculate test statistic
        std_error = math.sqrt(null_proportion * (1 - null_proportion) / sample_size)
        z_stat = (sample_proportion - null_proportion) / std_error
        
        # Critical values and p-value
        if test_type == 'two-tailed':
            critical_values = [-stats.norm.ppf(1 - alpha/2), stats.norm.ppf(1 - alpha/2)]
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        elif test_type == 'left-tailed':
            critical_values = [stats.norm.ppf(alpha)]
            p_value = stats.norm.cdf(z_stat)
        else:  # right-tailed
            critical_values = [stats.norm.ppf(1 - alpha)]
            p_value = 1 - stats.norm.cdf(z_stat)
        
        # Decision
        if test_type == 'two-tailed':
            reject_null = abs(z_stat) > abs(critical_values[1])
        elif test_type == 'left-tailed':
            reject_null = z_stat < critical_values[0]
        else:  # right-tailed
            reject_null = z_stat > critical_values[0]
        
        steps = [
            f"Step 1: State the hypotheses",
            f"{h0}",
            f"{h1}",
            f"Step 2: Check normal approximation conditions",
            f"np₀ = {sample_size} × {null_proportion} = {np0}",
            f"nq₀ = n(1-p₀) = {sample_size} × {1-null_proportion} = {nq0}",
            f"Both np₀ ≥ 5 and nq₀ ≥ 5? {'Yes' if np0 >= 5 and nq0 >= 5 else 'No'}",
            f"Step 3: Set significance level α = {alpha}",
            f"Step 4: Calculate test statistic",
            f"Given: p̂ = {sample_proportion}, p₀ = {null_proportion}, n = {sample_size}",
            f"SE = √[p₀(1-p₀)/n] = √[{null_proportion} × {1-null_proportion} / {sample_size}] = {std_error}",
            f"z = (p̂ - p₀)/SE = ({sample_proportion} - {null_proportion})/{std_error} = {z_stat}",
            f"Step 5: Find critical value(s) and p-value",
            f"Critical value(s): {critical_values}",
            f"p-value = {p_value}",
            f"Step 6: Make decision",
            f"Since p-value ({p_value}) {'<' if reject_null else '≥'} α ({alpha}), we {'reject' if reject_null else 'fail to reject'} H₀"
        ]
        
        return {
            'test_statistic': z_stat,
            'critical_values': critical_values,
            'p_value': p_value,
            'alpha': alpha,
            'reject_null': reject_null,
            'standard_error': std_error,
            'test_type': test_type,
            'null_hypothesis': h0,
            'alternative_hypothesis': h1,
            'sample_proportion': sample_proportion,
            'sample_size': sample_size,
            'null_proportion': null_proportion,
            'formula': 'z = (p̂ - p₀) / √[p₀(1-p₀)/n]',
            'steps': steps,
            'conclusion': f"{'Reject' if reject_null else 'Fail to reject'} the null hypothesis at α = {alpha} level",
            'interpretation': f"There {'is' if reject_null else '