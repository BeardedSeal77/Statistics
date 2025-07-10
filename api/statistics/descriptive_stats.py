# api/statistics/descriptive_stats.py
import numpy as np
from scipy import stats
from typing import List, Dict, Any, Optional
import json

class DescriptiveStats:
    """
    A comprehensive class for calculating descriptive statistics
    with detailed step-by-step explanations and formulas.
    """
    
    def __init__(self, data: List[float]):
        """
        Initialize with dataset
        
        Args:
            data: List of numerical values
        """
        self.data = np.array(data)
        self.n = len(data)
        self.sorted_data = np.sort(self.data)
        
    def calculate_all_stats(self, custom_percentile: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate all descriptive statistics with explanations
        
        Args:
            custom_percentile: Custom percentile to calculate (0-100)
            
        Returns:
            Dictionary containing all statistics, formulas, and steps
        """
        results = {
            'data_info': {
                'original_data': self.data.tolist(),
                'sorted_data': self.sorted_data.tolist(),
                'sample_size': self.n
            },
            'measures_of_central_tendency': self._calculate_central_tendency(),
            'measures_of_dispersion': self._calculate_dispersion(),
            'measures_of_position': self._calculate_position(),
            'distribution_shape': self._calculate_shape(),
            'five_number_summary': self._calculate_five_number_summary()
        }
        
        # Add custom percentile if provided
        if custom_percentile is not None:
            results['custom_percentile'] = self._calculate_custom_percentile(custom_percentile)
            
        return results
    
    def _calculate_central_tendency(self) -> Dict[str, Any]:
        """Calculate mean, median, and mode with explanations"""
        
        # Mean calculation
        mean_value = np.mean(self.data)
        mean_steps = [
            f"Sum of all values: {' + '.join(map(str, self.data))} = {np.sum(self.data)}",
            f"Number of values: n = {self.n}",
            f"Mean = Sum / n = {np.sum(self.data)} / {self.n} = {mean_value}"
        ]
        
        # Median calculation
        median_value = np.median(self.data)
        if self.n % 2 == 1:
            median_steps = [
                f"Sorted data: {self.sorted_data.tolist()}",
                f"n = {self.n} (odd), so median is the middle value",
                f"Position = (n + 1) / 2 = ({self.n} + 1) / 2 = {(self.n + 1) // 2}",
                f"Median = {median_value}"
            ]
        else:
            mid1, mid2 = self.sorted_data[self.n//2 - 1], self.sorted_data[self.n//2]
            median_steps = [
                f"Sorted data: {self.sorted_data.tolist()}",
                f"n = {self.n} (even), so median is average of two middle values",
                f"Middle values: {mid1} and {mid2}",
                f"Median = ({mid1} + {mid2}) / 2 = {median_value}"
            ]
        
        # Mode calculation
        mode_result = stats.mode(self.data, keepdims=True)
        mode_value = mode_result.mode[0] if mode_result.count[0] > 1 else None
        mode_count = mode_result.count[0] if mode_result.count[0] > 1 else 0
        
        if mode_value is not None:
            mode_steps = [
                f"Count frequency of each value:",
                *[f"  {val}: {np.sum(self.data == val)} times" for val in np.unique(self.data)],
                f"Mode = {mode_value} (appears {mode_count} times)"
            ]
        else:
            mode_steps = ["No mode exists (all values appear with equal frequency)"]
        
        return {
            'mean': {
                'value': mean_value,
                'formula': 'x̄ = Σx / n',
                'steps': mean_steps,
                'description': 'The arithmetic average of all values'
            },
            'median': {
                'value': median_value,
                'formula': 'Middle value when data is arranged in order',
                'steps': median_steps,
                'description': 'The middle value that separates the higher half from the lower half'
            },
            'mode': {
                'value': mode_value,
                'formula': 'Most frequently occurring value',
                'steps': mode_steps,
                'description': 'The value that appears most frequently in the dataset'
            }
        }
    
    def _calculate_dispersion(self) -> Dict[str, Any]:
        """Calculate variance, standard deviation, and range"""
        
        mean_value = np.mean(self.data)
        
        # Sample variance and standard deviation
        sample_var = np.var(self.data, ddof=1)
        sample_std = np.std(self.data, ddof=1)
        
        # Population variance and standard deviation
        pop_var = np.var(self.data, ddof=0)
        pop_std = np.std(self.data, ddof=0)
        
        # Range
        range_value = np.max(self.data) - np.min(self.data)
        
        # Variance calculation steps
        deviations = self.data - mean_value
        squared_deviations = deviations ** 2
        
        sample_var_steps = [
            f"Mean (x̄) = {mean_value}",
            f"Deviations from mean: {deviations.tolist()}",
            f"Squared deviations: {squared_deviations.tolist()}",
            f"Sum of squared deviations: {np.sum(squared_deviations)}",
            f"Sample variance = Σ(x - x̄)² / (n - 1) = {np.sum(squared_deviations)} / {self.n - 1} = {sample_var}",
            f"Sample standard deviation = √{sample_var} = {sample_std}"
        ]
        
        pop_var_steps = [
            f"Population variance = Σ(x - x̄)² / n = {np.sum(squared_deviations)} / {self.n} = {pop_var}",
            f"Population standard deviation = √{pop_var} = {pop_std}"
        ]
        
        return {
            'sample_variance': {
                'value': sample_var,
                'formula': 's² = Σ(x - x̄)² / (n - 1)',
                'steps': sample_var_steps,
                'description': 'Sample variance (divides by n-1 for unbiased estimate)'
            },
            'sample_std_dev': {
                'value': sample_std,
                'formula': 's = √[Σ(x - x̄)² / (n - 1)]',
                'steps': [f"Sample standard deviation = √{sample_var} = {sample_std}"],
                'description': 'Sample standard deviation (square root of sample variance)'
            },
            'population_variance': {
                'value': pop_var,
                'formula': 'σ² = Σ(x - μ)² / n',
                'steps': pop_var_steps,
                'description': 'Population variance (divides by n)'
            },
            'population_std_dev': {
                'value': pop_std,
                'formula': 'σ = √[Σ(x - μ)² / n]',
                'steps': [f"Population standard deviation = √{pop_var} = {pop_std}"],
                'description': 'Population standard deviation (square root of population variance)'
            },
            'range': {
                'value': range_value,
                'formula': 'Range = Maximum - Minimum',
                'steps': [f"Range = {np.max(self.data)} - {np.min(self.data)} = {range_value}"],
                'description': 'The difference between the largest and smallest values'
            }
        }
    
    def _calculate_position(self) -> Dict[str, Any]:
        """Calculate percentiles and quartiles"""
        
        q1 = np.percentile(self.data, 25)
        q2 = np.percentile(self.data, 50)  # Same as median
        q3 = np.percentile(self.data, 75)
        
        percentiles = {
            'q1': {
                'value': q1,
                'formula': 'Q1 = 25th percentile',
                'steps': [f"Q1 (25th percentile) = {q1}"],
                'description': 'First quartile - 25% of data falls below this value'
            },
            'q2': {
                'value': q2,
                'formula': 'Q2 = 50th percentile = Median',
                'steps': [f"Q2 (50th percentile) = {q2}"],
                'description': 'Second quartile - same as median'
            },
            'q3': {
                'value': q3,
                'formula': 'Q3 = 75th percentile',
                'steps': [f"Q3 (75th percentile) = {q3}"],
                'description': 'Third quartile - 75% of data falls below this value'
            }
        }
        
        return percentiles
    
    def _calculate_shape(self) -> Dict[str, Any]:
        """Calculate skewness and kurtosis"""
        
        skewness = stats.skew(self.data)
        kurtosis = stats.kurtosis(self.data)
        
        # Interpret skewness
        if abs(skewness) < 0.5:
            skew_interpretation = "Approximately symmetric"
        elif skewness > 0:
            skew_interpretation = "Right-skewed (positively skewed)"
        else:
            skew_interpretation = "Left-skewed (negatively skewed)"
        
        # Interpret kurtosis
        if abs(kurtosis) < 0.5:
            kurt_interpretation = "Approximately normal (mesokurtic)"
        elif kurtosis > 0:
            kurt_interpretation = "Heavy-tailed (leptokurtic)"
        else:
            kurt_interpretation = "Light-tailed (platykurtic)"
        
        return {
            'skewness': {
                'value': skewness,
                'formula': 'Skewness = E[(X - μ)³] / σ³',
                'interpretation': skew_interpretation,
                'description': 'Measures asymmetry of the distribution'
            },
            'kurtosis': {
                'value': kurtosis,
                'formula': 'Kurtosis = E[(X - μ)⁴] / σ⁴ - 3',
                'interpretation': kurt_interpretation,
                'description': 'Measures tail heaviness relative to normal distribution'
            }
        }
    
    def _calculate_five_number_summary(self) -> Dict[str, Any]:
        """Calculate five-number summary and IQR"""
        
        minimum = np.min(self.data)
        q1 = np.percentile(self.data, 25)
        median = np.median(self.data)
        q3 = np.percentile(self.data, 75)
        maximum = np.max(self.data)
        iqr = q3 - q1
        
        return {
            'minimum': minimum,
            'q1': q1,
            'median': median,
            'q3': q3,
            'maximum': maximum,
            'iqr': {
                'value': iqr,
                'formula': 'IQR = Q3 - Q1',
                'steps': [f"IQR = {q3} - {q1} = {iqr}"],
                'description': 'Interquartile range - spread of middle 50% of data'
            }
        }
    
    def _calculate_custom_percentile(self, percentile: float) -> Dict[str, Any]:
        """Calculate custom percentile"""
        
        value = np.percentile(self.data, percentile)
        
        return {
            'percentile': percentile,
            'value': value,
            'formula': f'{percentile}th percentile',
            'steps': [f"{percentile}th percentile = {value}"],
            'description': f'{percentile}% of the data falls below this value'
        }
    
    def calculate_standard_error(self, confidence_level: float = 0.95) -> Dict[str, Any]:
        """Calculate standard error of the mean"""
        
        sample_std = np.std(self.data, ddof=1)
        std_error = sample_std / np.sqrt(self.n)
        
        # Critical value for confidence interval
        alpha = 1 - confidence_level
        t_critical = stats.t.ppf(1 - alpha/2, self.n - 1)
        
        margin_of_error = t_critical * std_error
        
        return {
            'standard_error': {
                'value': std_error,
                'formula': 'SE = s / √n',
                'steps': [
                    f"Sample standard deviation (s) = {sample_std}",
                    f"Sample size (n) = {self.n}",
                    f"Standard error = {sample_std} / √{self.n} = {std_error}"
                ],
                'description': 'Standard error of the sample mean'
            },
            'margin_of_error': {
                'value': margin_of_error,
                'formula': f'ME = t₀.₀₂₅ × SE',
                'steps': [
                    f"Confidence level = {confidence_level * 100}%",
                    f"Degrees of freedom = {self.n - 1}",
                    f"t-critical value = {t_critical}",
                    f"Margin of error = {t_critical} × {std_error} = {margin_of_error}"
                ],
                'description': f'Margin of error for {confidence_level * 100}% confidence interval'
            }
        }