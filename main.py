#!/usr/bin/env python3
"""
Statistics Calculator Console Application
A comprehensive statistical analysis tool with step-by-step solutions.
"""

import os
import sys
from typing import List, Optional, Dict, Any

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classes.descriptive_stats import DescriptiveStats
from classes.normal_distribution import NormalDistribution
from classes.confidence_intervals import ConfidenceIntervals
from classes.hypothesis_testing import HypothesisTesting
from utils.input_helpers import *
from utils.display_helpers import *

class StatisticsCalculator:
    """Main calculator class that handles the console interface"""
    
    def __init__(self):
        self.decimal_places = 4
        self.clear_screen()
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display the application header"""
        print("=" * 70)
        print("           📊 STATISTICS CALCULATOR CONSOLE 📊")
        print("     Comprehensive Statistical Analysis with Step-by-Step Solutions")
        print("=" * 70)
        print(f"Current decimal places: {self.decimal_places}")
        print("-" * 70)
    
    def main_menu(self):
        """Display and handle the main menu"""
        while True:
            self.clear_screen()
            self.display_header()
            
            print("\n🔢 SELECT ANALYSIS TYPE:")
            print("1. Descriptive Statistics")
            print("2. Normal Distribution")
            print("3. Confidence Intervals")
            print("4. Hypothesis Testing")
            print("5. Settings (Decimal Places)")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.descriptive_statistics_menu()
            elif choice == '2':
                self.normal_distribution_menu()
            elif choice == '3':
                self.confidence_intervals_menu()
            elif choice == '4':
                self.hypothesis_testing_menu()
            elif choice == '5':
                self.settings_menu()
            elif choice == '6':
                print("\n👋 Thank you for using Statistics Calculator!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    def descriptive_statistics_menu(self):
        """Handle descriptive statistics calculations"""
        self.clear_screen()
        self.display_header()
        print("\n📊 DESCRIPTIVE STATISTICS")
        print("-" * 40)
        
        # Get dataset
        data = get_dataset()
        if not data:
            return
        
        # Get custom percentile (optional)
        custom_percentile = get_custom_percentile()
        
        # Calculate statistics
        stats_calc = DescriptiveStats(data)
        results = stats_calc.calculate_all_stats(custom_percentile)
        
        # Add standard error analysis
        include_se = get_yes_no("Include standard error analysis? (y/n): ")
        if include_se:
            confidence_level = get_float("Enter confidence level (0-1, default 0.95): ", 0.95)
            se_results = stats_calc.calculate_standard_error(confidence_level)
            results['standard_error_analysis'] = se_results
        
        # Display results
        self.display_descriptive_results(results)
        
        input("\nPress Enter to continue...")
    
    def normal_distribution_menu(self):
        """Handle normal distribution calculations"""
        self.clear_screen()
        self.display_header()
        print("\n📈 NORMAL DISTRIBUTION")
        print("-" * 40)
        
        # Get distribution parameters
        mean = get_float("Enter mean (μ): ")
        std_dev = get_positive_float("Enter standard deviation (σ): ")
        
        norm_dist = NormalDistribution(mean, std_dev)
        
        # Get calculation type
        calc_types = {
            '1': 'Z-Score Calculation',
            '2': 'Probability Calculation',
            '3': 'Probability Between Values',
            '4': 'Find Percentile Value',
            '5': 'Critical Values',
            '6': 'Empirical Rule (68-95-99.7)'
        }
        
        print("\nSelect calculation type:")
        for key, value in calc_types.items():
            print(f"{key}. {value}")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        results = None
        
        if choice == '1':  # Z-Score
            x_value = get_float("Enter x-value: ")
            results = norm_dist.calculate_z_score(x_value)
            
        elif choice == '2':  # Probability
            x_value = get_float("Enter x-value: ")
            comparison = get_comparison_type()
            results = norm_dist.calculate_probability(x_value, comparison)
            
        elif choice == '3':  # Probability Between
            x1 = get_float("Enter lower bound (x1): ")
            x2 = get_float("Enter upper bound (x2): ")
            results = norm_dist.calculate_probability_between(x1, x2)
            
        elif choice == '4':  # Percentile
            percentile = get_percentile()
            results = norm_dist.find_percentile(percentile)
            
        elif choice == '5':  # Critical Values
            confidence_level = get_confidence_level()
            results = norm_dist.find_critical_values(confidence_level)
            
        elif choice == '6':  # Empirical Rule
            results = norm_dist.empirical_rule()
            
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            return
        
        if results:
            self.display_normal_results(results, choice)
        
        input("\nPress Enter to continue...")
    
    def confidence_intervals_menu(self):
        """Handle confidence interval calculations"""
        self.clear_screen()
        self.display_header()
        print("\n🎯 CONFIDENCE INTERVALS")
        print("-" * 40)
        
        ci_calc = ConfidenceIntervals()
        
        # Get interval type
        interval_types = {
            '1': 'Mean Confidence Interval',
            '2': 'Proportion Confidence Interval',
            '3': 'Sample Size for Mean',
            '4': 'Sample Size for Proportion'
        }
        
        print("Select interval type:")
        for key, value in interval_types.items():
            print(f"{key}. {value}")
        
        choice = input("\nEnter choice (1-4): ").strip()
        results = None
        
        if choice == '1':  # Mean CI
            sample_mean = get_float("Enter sample mean (x̄): ")
            sample_size = get_positive_int("Enter sample size (n): ")
            confidence_level = get_confidence_level()
            
            # Ask for population or sample std dev
            has_pop_std = get_yes_no("Do you know the population standard deviation? (y/n): ")
            
            if has_pop_std:
                pop_std = get_positive_float("Enter population standard deviation (σ): ")
                results = ci_calc.mean_confidence_interval(
                    sample_mean, sample_size, confidence_level, population_std=pop_std
                )
            else:
                sample_std = get_positive_float("Enter sample standard deviation (s): ")
                results = ci_calc.mean_confidence_interval(
                    sample_mean, sample_size, confidence_level, sample_std=sample_std
                )
                
        elif choice == '2':  # Proportion CI
            sample_prop = get_proportion("Enter sample proportion (p̂): ")
            sample_size = get_positive_int("Enter sample size (n): ")
            confidence_level = get_confidence_level()
            
            results = ci_calc.proportion_confidence_interval(sample_prop, sample_size, confidence_level)
            
        elif choice == '3':  # Sample Size for Mean
            margin_error = get_positive_float("Enter desired margin of error: ")
            confidence_level = get_confidence_level()
            pop_std = get_positive_float("Enter population standard deviation (σ): ")
            
            results = ci_calc.sample_size_for_mean(margin_error, confidence_level, pop_std)
            
        elif choice == '4':  # Sample Size for Proportion
            margin_error = get_positive_float("Enter desired margin of error: ")
            confidence_level = get_confidence_level()
            
            has_estimate = get_yes_no("Do you have a prior proportion estimate? (y/n): ")
            estimated_prop = None
            if has_estimate:
                estimated_prop = get_proportion("Enter estimated proportion: ")
            
            results = ci_calc.sample_size_for_proportion(margin_error, confidence_level, estimated_prop)
            
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            return
        
        if results:
            self.display_ci_results(results, choice)
        
        input("\nPress Enter to continue...")
    
    def hypothesis_testing_menu(self):
        """Handle hypothesis testing calculations"""
        self.clear_screen()
        self.display_header()
        print("\n🔬 HYPOTHESIS TESTING")
        print("-" * 40)
        
        ht_calc = HypothesisTesting()
        
        # Get test type
        test_types = {
            '1': 'One-Sample Mean Test',
            '2': 'One-Sample Proportion Test',
            '3': 'Two-Sample Mean Test',
            '4': 'Two-Sample Proportion Test'
        }
        
        print("Select test type:")
        for key, value in test_types.items():
            print(f"{key}. {value}")
        
        choice = input("\nEnter choice (1-4): ").strip()
        results = None
        
        alpha = get_alpha()
        test_type = get_tail_type()
        
        if choice == '1':  # One-Sample Mean
            sample_mean = get_float("Enter sample mean (x̄): ")
            sample_size = get_positive_int("Enter sample size (n): ")
            null_mean = get_float("Enter null hypothesis mean (μ₀): ")
            
            has_pop_std = get_yes_no("Do you know the population standard deviation? (y/n): ")
            
            if has_pop_std:
                pop_std = get_positive_float("Enter population standard deviation (σ): ")
                results = ht_calc.one_sample_mean_test(
                    sample_mean, sample_size, null_mean, alpha, test_type, population_std=pop_std
                )
            else:
                sample_std = get_positive_float("Enter sample standard deviation (s): ")
                results = ht_calc.one_sample_mean_test(
                    sample_mean, sample_size, null_mean, alpha, test_type, sample_std=sample_std
                )
                
        elif choice == '2':  # One-Sample Proportion
            sample_prop = get_proportion("Enter sample proportion (p̂): ")
            sample_size = get_positive_int("Enter sample size (n): ")
            null_prop = get_proportion("Enter null hypothesis proportion (p₀): ")
            
            results = ht_calc.one_sample_proportion_test(sample_prop, sample_size, null_prop, alpha, test_type)
            
        elif choice == '3':  # Two-Sample Mean
            print("\nSample 1:")
            sample1_mean = get_float("Enter sample 1 mean (x̄₁): ")
            sample1_size = get_positive_int("Enter sample 1 size (n₁): ")
            sample1_std = get_positive_float("Enter sample 1 std dev (s₁): ")
            
            print("\nSample 2:")
            sample2_mean = get_float("Enter sample 2 mean (x̄₂): ")
            sample2_size = get_positive_int("Enter sample 2 size (n₂): ")
            sample2_std = get_positive_float("Enter sample 2 std dev (s₂): ")
            
            equal_var = get_yes_no("Assume equal variances? (y/n): ")
            
            results = ht_calc.two_sample_mean_test(
                sample1_mean, sample1_size, sample1_std,
                sample2_mean, sample2_size, sample2_std,
                alpha, test_type, equal_var
            )
            
        elif choice == '4':  # Two-Sample Proportion
            print("\nSample 1:")
            sample1_successes = get_positive_int("Enter sample 1 successes: ")
            sample1_size = get_positive_int("Enter sample 1 size (n₁): ")
            
            print("\nSample 2:")
            sample2_successes = get_positive_int("Enter sample 2 successes: ")
            sample2_size = get_positive_int("Enter sample 2 size (n₂): ")
            
            results = ht_calc.two_sample_proportion_test(
                sample1_successes, sample1_size, sample2_successes, sample2_size, alpha, test_type
            )
            
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            return
        
        if results:
            self.display_hypothesis_results(results)
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Handle settings (decimal places)"""
        self.clear_screen()
        self.display_header()
        print("\n⚙️  SETTINGS")
        print("-" * 40)
        
        print(f"Current decimal places: {self.decimal_places}")
        new_decimals = get_int_in_range("Enter new decimal places (0-10): ", 0, 10)
        if new_decimals is not None:
            self.decimal_places = new_decimals
            print(f"✅ Decimal places updated to {self.decimal_places}")
        
        input("Press Enter to continue...")
    
    def display_descriptive_results(self, results: Dict[str, Any]):
        """Display descriptive statistics results"""
        self.clear_screen()
        print("📊 DESCRIPTIVE STATISTICS RESULTS")
        print("=" * 50)
        
        # Data info
        data_info = results['data_info']
        print(f"\n📋 Dataset Information:")
        print(f"   Sample Size: {data_info['sample_size']}")
        print(f"   Original Data: {data_info['original_data']}")
        print(f"   Sorted Data: {data_info['sorted_data']}")
        
        # Central tendency
        print(f"\n📊 Measures of Central Tendency:")
        central = results['measures_of_central_tendency']
        self._display_stat_with_steps("Mean", central['mean'])
        self._display_stat_with_steps("Median", central['median'])
        self._display_stat_with_steps("Mode", central['mode'])
        
        # Dispersion
        print(f"\n📏 Measures of Dispersion:")
        dispersion = results['measures_of_dispersion']
        self._display_stat_with_steps("Sample Variance", dispersion['sample_variance'])
        self._display_stat_with_steps("Sample Std Dev", dispersion['sample_std_dev'])
        self._display_stat_with_steps("Range", dispersion['range'])
        
        # Position
        print(f"\n📍 Measures of Position:")
        position = results['measures_of_position']
        self._display_stat_with_steps("Q1 (25th percentile)", position['q1'])
        self._display_stat_with_steps("Q2 (50th percentile)", position['q2'])
        self._display_stat_with_steps("Q3 (75th percentile)", position['q3'])
        
        # Custom percentile
        if 'custom_percentile' in results:
            custom = results['custom_percentile']
            self._display_stat_with_steps(f"{custom['percentile']}th Percentile", custom)
        
        # Five number summary
        print(f"\n📋 Five-Number Summary:")
        summary = results['five_number_summary']
        print(f"   Min: {summary['minimum']}")
        print(f"   Q1:  {summary['q1']}")
        print(f"   Med: {summary['median']}")
        print(f"   Q3:  {summary['q3']}")
        print(f"   Max: {summary['maximum']}")
        self._display_stat_with_steps("IQR", summary['iqr'])
        
        # Distribution shape
        print(f"\n📈 Distribution Shape:")
        shape = results['distribution_shape']
        print(f"   Skewness: {round(shape['skewness']['value'], self.decimal_places)} ({shape['skewness']['interpretation']})")
        print(f"   Kurtosis: {round(shape['kurtosis']['value'], self.decimal_places)} ({shape['kurtosis']['interpretation']})")
        
        # Standard error analysis
        if 'standard_error_analysis' in results:
            print(f"\n🎯 Standard Error Analysis:")
            se = results['standard_error_analysis']
            self._display_stat_with_steps("Standard Error", se['standard_error'])
            self._display_stat_with_steps("Margin of Error", se['margin_of_error'])
    
    def display_normal_results(self, results: Dict[str, Any], choice: str):
        """Display normal distribution results"""
        self.clear_screen()
        print("📈 NORMAL DISTRIBUTION RESULTS")
        print("=" * 50)
        
        if 'formula' in results:
            print(f"\n📐 Formula: {results['formula']}")
        
        # Display main result
        if choice == '1':  # Z-Score
            print(f"\n🎯 Z-Score: {round(results['z_score'], self.decimal_places)}")
            print(f"   Interpretation: {results['interpretation']}")
        elif choice == '2':  # Probability
            print(f"\n🎯 Probability: {round(results['probability'], self.decimal_places)}")
            print(f"   Percentage: {round(results['percentage'], 2)}%")
            print(f"   Z-Score: {round(results['z_score'], self.decimal_places)}")
        elif choice == '6':  # Empirical Rule
            print(f"\n🎯 Empirical Rule Boundaries:")
            print(f"   68% within: [{round(results['one_std']['lower'], self.decimal_places)}, {round(results['one_std']['upper'], self.decimal_places)}]")
            print(f"   95% within: [{round(results['two_std']['lower'], self.decimal_places)}, {round(results['two_std']['upper'], self.decimal_places)}]")
            print(f"   99.7% within: [{round(results['three_std']['lower'], self.decimal_places)}, {round(results['three_std']['upper'], self.decimal_places)}]")
        
        # Display steps
        if 'steps' in results:
            print(f"\n📝 Step-by-Step Solution:")
            for i, step in enumerate(results['steps'], 1):
                print(f"   {i}. {step}")
        
        if 'description' in results:
            print(f"\n💡 Description: {results['description']}")
    
    def display_ci_results(self, results: Dict[str, Any], choice: str):
        """Display confidence interval results"""
        self.clear_screen()
        print("🎯 CONFIDENCE INTERVAL RESULTS")
        print("=" * 50)
        
        if 'formula' in results:
            print(f"\n📐 Formula: {results['formula']}")
        
        # Display main result
        if choice in ['1', '2']:  # CI results
            if 'confidence_interval' in results:
                ci = results['confidence_interval']
                print(f"\n🎯 {round(results['confidence_level'] * 100, 1)}% Confidence Interval:")
                print(f"   [{round(ci[0], self.decimal_places)}, {round(ci[1], self.decimal_places)}]")
                print(f"   Margin of Error: {round(results['margin_of_error'], self.decimal_places)}")
        elif choice in ['3', '4']:  # Sample size results
            print(f"\n🎯 Required Sample Size: {results['sample_size_required']}")
            print(f"   Exact calculation: {round(results['sample_size_exact'], self.decimal_places)}")
        
        # Display steps
        if 'steps' in results:
            print(f"\n📝 Step-by-Step Solution:")
            for i, step in enumerate(results['steps'], 1):
                print(f"   {i}. {step}")
        
        if 'interpretation' in results:
            print(f"\n💡 Interpretation: {results['interpretation']}")
        
        if 'warning' in results and results['warning']:
            print(f"\n⚠️  Warning: {results['warning']}")
    
    def display_hypothesis_results(self, results: Dict[str, Any]):
        """Display hypothesis testing results"""
        self.clear_screen()
        print("🔬 HYPOTHESIS TESTING RESULTS")
        print("=" * 50)
        
        # Hypotheses
        print(f"\n📋 Hypotheses:")
        print(f"   {results['null_hypothesis']}")
        print(f"   {results['alternative_hypothesis']}")
        
        # Test results
        print(f"\n🎯 Test Results:")
        print(f"   Test Statistic: {round(results['test_statistic'], self.decimal_places)}")
        print(f"   P-value: {round(results['p_value'], self.decimal_places)}")
        print(f"   Critical Value(s): {[round(cv, self.decimal_places) for cv in results['critical_values']]}")
        print(f"   α (alpha): {results['alpha']}")
        
        # Decision
        decision = "REJECT" if results['reject_null'] else "FAIL TO REJECT"
        print(f"\n⚖️  Decision: {decision} the null hypothesis")
        print(f"   Conclusion: {results['conclusion']}")
        
        # Steps
        if 'steps' in results:
            print(f"\n📝 Step-by-Step Solution:")
            for i, step in enumerate(results['steps'], 1):
                print(f"   {i}. {step}")
        
        if 'interpretation' in results:
            print(f"\n💡 Interpretation: {results['interpretation']}")
        
        if 'warning' in results and results['warning']:
            print(f"\n⚠️  Warning: {results['warning']}")
    
    def _display_stat_with_steps(self, name: str, stat_data: Dict[str, Any]):
        """Helper to display a statistic with its value and optional steps"""
        value = stat_data.get('value')
        if value is not None:
            if isinstance(value, (int, float)):
                rounded_value = round(value, self.decimal_places)
                print(f"   {name}: {value} (rounded: {rounded_value})")
            else:
                print(f"   {name}: {value}")
        
        if stat_data.get('description'):
            print(f"      Description: {stat_data['description']}")
        
        # Optionally show steps (you can uncomment this if you want to see calculation steps)
        # if stat_data.get('steps'):
        #     print(f"      Steps:")
        #     for step in stat_data['steps']:
        #         print(f"        - {step}")


def main():
    """Main function to run the calculator"""
    try:
        calculator = StatisticsCalculator()
        calculator.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the application.")


if __name__ == "__main__":
    main()