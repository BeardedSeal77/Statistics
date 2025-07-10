# api/routes/stats_routes.py
from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
import json

# Import our statistics classes
from ..statistics.descriptive_stats import DescriptiveStats
from ..statistics.normal_distribution import NormalDistribution
from ..statistics.confidence_intervals import ConfidenceIntervals
from ..statistics.hypothesis_testing import HypothesisTesting

# Create blueprint
stats_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

def round_result(value, decimals: int):
    """Helper function to round numerical values"""
    if isinstance(value, (int, float)):
        return round(value, decimals)
    elif isinstance(value, list):
        return [round_result(item, decimals) for item in value]
    elif isinstance(value, dict):
        return {key: round_result(val, decimals) for key, val in value.items()}
    else:
        return value

def apply_rounding(data: Dict[str, Any], decimals: int) -> Dict[str, Any]:
    """Apply rounding to all numerical values in the result"""
    rounded_data = {}
    for key, value in data.items():
        if key in ['steps', 'formula', 'description', 'interpretation', 'conclusion', 
                   'null_hypothesis', 'alternative_hypothesis', 'warning']:
            # Don't round text fields
            rounded_data[key] = value
        else:
            rounded_data[key] = round_result(value, decimals)
    
    # Create rounded display versions
    rounded_data['rounded_display'] = round_result(data, decimals)
    return rounded_data

@stats_bp.route('/descriptive', methods=['POST'])
def calculate_descriptive_stats():
    """Calculate descriptive statistics for a dataset"""
    try:
        data = request.get_json()
        
        # Extract parameters
        dataset = data.get('data', [])
        custom_percentile = data.get('custom_percentile')
        decimals = data.get('decimals', 4)
        
        if not dataset or not isinstance(dataset, list):
            return jsonify({'error': 'Invalid dataset provided'}), 400
        
        # Validate data
        try:
            numeric_data = [float(x) for x in dataset]
        except (ValueError, TypeError):
            return jsonify({'error': 'All data values must be numeric'}), 400
        
        # Calculate statistics
        stats_calc = DescriptiveStats(numeric_data)
        results = stats_calc.calculate_all_stats(custom_percentile)
        
        # Add standard error if requested
        if data.get('include_standard_error', False):
            confidence_level = data.get('confidence_level', 0.95)
            se_results = stats_calc.calculate_standard_error(confidence_level)
            results['standard_error_analysis'] = se_results
        
        # Apply rounding
        final_results = apply_rounding(results, decimals)
        
        return jsonify({
            'success': True,
            'results': final_results,
            'input_parameters': {
                'dataset': dataset,
                'custom_percentile': custom_percentile,
                'decimals': decimals
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stats_bp.route('/normal-distribution', methods=['POST'])
def normal_distribution_calculations():
    """Perform normal distribution calculations"""
    try:
        data = request.get_json()
        
        # Extract parameters
        mean = data.get('mean')
        std_dev = data.get('std_dev')
        calculation_type = data.get('calculation_type')
        decimals = data.get('decimals', 4)
        
        if mean is None or std_dev is None:
            return jsonify({'error': 'Mean and standard deviation are required'}), 400
        
        if std_dev <= 0:
            return jsonify({'error': 'Standard deviation must be positive'}), 400
        
        # Create normal distribution object
        norm_dist = NormalDistribution(float(mean), float(std_dev))
        
        results = {}
        
        if calculation_type == 'z_score':
            x_value = data.get('x_value')
            if x_value is None:
                return jsonify({'error': 'x_value is required for z-score calculation'}), 400
            results = norm_dist.calculate_z_score(float(x_value))
            
        elif calculation_type == 'probability':
            x_value = data.get('x_value')
            comparison = data.get('comparison', 'less_than')
            if x_value is None:
                return jsonify({'error': 'x_value is required for probability calculation'}), 400
            results = norm_dist.calculate_probability(float(x_value), comparison)
            
        elif calculation_type == 'probability_between':
            x1 = data.get('x1')
            x2 = data.get('x2')
            if x1 is None or x2 is None:
                return jsonify({'error': 'x1 and x2 are required for between probability'}), 400
            results = norm_dist.calculate_probability_between(float(x1), float(x2))
            
        elif calculation_type == 'percentile':
            percentile = data.get('percentile')
            if percentile is None:
                return jsonify({'error': 'percentile is required'}), 400
            if not 0 < percentile < 100:
                return jsonify({'error': 'percentile must be between 0 and 100'}), 400
            results = norm_dist.find_percentile(float(percentile))
            
        elif calculation_type == 'critical_values':
            confidence_level = data.get('confidence_level')
            if confidence_level is None:
                return jsonify({'error': 'confidence_level is required'}), 400
            if not 0 < confidence_level < 1:
                return jsonify({'error': 'confidence_level must be between 0 and 1'}), 400
            results = norm_dist.find_critical_values(float(confidence_level))
            
        elif calculation_type == 'empirical_rule':
            results = norm_dist.empirical_rule()
            
        else:
            return jsonify({'error': 'Invalid calculation_type'}), 400
        
        # Apply rounding
        final_results = apply_rounding(results, decimals)
        
        return jsonify({
            'success': True,
            'results': final_results,
            'input_parameters': {
                'mean': mean,
                'std_dev': std_dev,
                'calculation_type': calculation_type,
                'decimals': decimals
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stats_bp.route('/confidence-intervals', methods=['POST'])
def confidence_interval_calculations():
    """Calculate confidence intervals"""
    try:
        data = request.get_json()
        
        # Extract parameters
        interval_type = data.get('interval_type')
        confidence_level = data.get('confidence_level')
        decimals = data.get('decimals', 4)
        
        if not interval_type or not confidence_level:
            return jsonify({'error': 'interval_type and confidence_level are required'}), 400
        
        if not 0 < confidence_level < 1:
            return jsonify({'error': 'confidence_level must be between 0 and 1'}), 400
        
        ci_calc = ConfidenceIntervals()
        results = {}
        
        if interval_type == 'mean':
            sample_mean = data.get('sample_mean')
            sample_size = data.get('sample_size')
            population_std = data.get('population_std')
            sample_std = data.get('sample_std')
            
            if sample_mean is None or sample_size is None:
                return jsonify({'error': 'sample_mean and sample_size are required'}), 400
            
            if population_std is None and sample_std is None:
                return jsonify({'error': 'Either population_std or sample_std must be provided'}), 400
            
            results = ci_calc.mean_confidence_interval(
                float(sample_mean), int(sample_size), float(confidence_level),
                float(population_std) if population_std is not None else None,
                float(sample_std) if sample_std is not None else None
            )
            
        elif interval_type == 'proportion':
            sample_proportion = data.get('sample_proportion')
            sample_size = data.get('sample_size')
            
            if sample_proportion is None or sample_size is None:
                return jsonify({'error': 'sample_proportion and sample_size are required'}), 400
            
            if not 0 <= sample_proportion <= 1:
                return jsonify({'error': 'sample_proportion must be between 0 and 1'}), 400
            
            results = ci_calc.proportion_confidence_interval(
                float(sample_proportion), int(sample_size), float(confidence_level)
            )
            
        elif interval_type == 'sample_size_mean':
            margin_error = data.get('margin_error')
            population_std = data.get('population_std')
            
            if margin_error is None or population_std is None:
                return jsonify({'error': 'margin_error and population_std are required'}), 400
            
            results = ci_calc.sample_size_for_mean(
                float(margin_error), float(confidence_level), float(population_std)
            )
            
        elif interval_type == 'sample_size_proportion':
            margin_error = data.get('margin_error')
            estimated_proportion = data.get('estimated_proportion')
            
            if margin_error is None:
                return jsonify({'error': 'margin_error is required'}), 400
            
            results = ci_calc.sample_size_for_proportion(
                float(margin_error), float(confidence_level),
                float(estimated_proportion) if estimated_proportion is not None else None
            )
            
        else:
            return jsonify({'error': 'Invalid interval_type'}), 400
        
        # Apply rounding
        final_results = apply_rounding(results, decimals)
        
        return jsonify({
            'success': True,
            'results': final_results,
            'input_parameters': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stats_bp.route('/hypothesis-testing', methods=['POST'])
def hypothesis_testing_calculations():
    """Perform hypothesis testing"""
    try:
        data = request.get_json()
        
        # Extract parameters
        test_type = data.get('test_type')
        alpha = data.get('alpha')
        tail_type = data.get('tail_type')
        decimals = data.get('decimals', 4)
        
        if not test_type or alpha is None or not tail_type:
            return jsonify({'error': 'test_type, alpha, and tail_type are required'}), 400
        
        if not 0 < alpha < 1:
            return jsonify({'error': 'alpha must be between 0 and 1'}), 400
        
        if tail_type not in ['two-tailed', 'left-tailed', 'right-tailed']:
            return jsonify({'error': 'tail_type must be two-tailed, left-tailed, or right-tailed'}), 400
        
        ht_calc = HypothesisTesting()
        results = {}
        
        if test_type == 'one_sample_mean':
            sample_mean = data.get('sample_mean')
            sample_size = data.get('sample_size')
            null_mean = data.get('null_mean')
            population_std = data.get('population_std')
            sample_std = data.get('sample_std')
            
            if any(x is None for x in [sample_mean, sample_size, null_mean]):
                return jsonify({'error': 'sample_mean, sample_size, and null_mean are required'}), 400
            
            if population_std is None and sample_std is None:
                return jsonify({'error': 'Either population_std or sample_std must be provided'}), 400
            
            results = ht_calc.one_sample_mean_test(
                float(sample_mean), int(sample_size), float(null_mean),
                float(alpha), tail_type,
                float(population_std) if population_std is not None else None,
                float(sample_std) if sample_std is not None else None
            )
            
        elif test_type == 'one_sample_proportion':
            sample_proportion = data.get('sample_proportion')
            sample_size = data.get('sample_size')
            null_proportion = data.get('null_proportion')
            
            if any(x is None for x in [sample_proportion, sample_size, null_proportion]):
                return jsonify({'error': 'sample_proportion, sample_size, and null_proportion are required'}), 400
            
            results = ht_calc.one_sample_proportion_test(
                float(sample_proportion), int(sample_size), float(null_proportion),
                float(alpha), tail_type
            )
            
        elif test_type == 'two_sample_mean':
            required_fields = ['sample1_mean', 'sample1_size', 'sample1_std',
                             'sample2_mean', 'sample2_size', 'sample2_std']
            
            if any(data.get(field) is None for field in required_fields):
                return jsonify({'error': f'All fields required: {required_fields}'}), 400
            
            equal_variances = data.get('equal_variances', True)
            
            results = ht_calc.two_sample_mean_test(
                float(data['sample1_mean']), int(data['sample1_size']), float(data['sample1_std']),
                float(data['sample2_mean']), int(data['sample2_size']), float(data['sample2_std']),
                float(alpha), tail_type, bool(equal_variances)
            )
            
        elif test_type == 'two_sample_proportion':
            required_fields = ['sample1_successes', 'sample1_size', 'sample2_successes', 'sample2_size']
            
            if any(data.get(field) is None for field in required_fields):
                return jsonify({'error': f'All fields required: {required_fields}'}), 400
            
            results = ht_calc.two_sample_proportion_test(
                int(data['sample1_successes']), int(data['sample1_size']),
                int(data['sample2_successes']), int(data['sample2_size']),
                float(alpha), tail_type
            )
            
        else:
            return jsonify({'error': 'Invalid test_type'}), 400
        
        # Apply rounding
        final_results = apply_rounding(results, decimals)
        
        return jsonify({
            'success': True,
            'results': final_results,
            'input_parameters': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stats_bp.route('/help', methods=['GET'])
def get_help():
    """Get help information about available endpoints and parameters"""
    help_info = {
        'endpoints': {
            '/descriptive': {
                'method': 'POST',
                'description': 'Calculate descriptive statistics for a dataset',
                'parameters': {
                    'data': 'List of numerical values (required)',
                    'custom_percentile': 'Custom percentile to calculate (0-100, optional)',
                    'include_standard_error': 'Include standard error analysis (boolean, optional)',
                    'confidence_level': 'Confidence level for standard error (0-1, default 0.95)',
                    'decimals': 'Number of decimal places for rounding (default 4)'
                },
                'example': {
                    'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'custom_percentile': 75,
                    'decimals': 3
                }
            },
            '/normal-distribution': {
                'method': 'POST',
                'description': 'Perform normal distribution calculations',
                'parameters': {
                    'mean': 'Population mean (required)',
                    'std_dev': 'Population standard deviation (required)',
                    'calculation_type': 'Type of calculation (required)',
                    'decimals': 'Number of decimal places for rounding (default 4)'
                },
                'calculation_types': {
                    'z_score': 'Calculate z-score for x_value',
                    'probability': 'Calculate probability (requires x_value, comparison)',
                    'probability_between': 'Calculate probability between x1 and x2',
                    'percentile': 'Find value at given percentile',
                    'critical_values': 'Find critical values for confidence level',
                    'empirical_rule': 'Calculate 68-95-99.7 rule boundaries'
                }
            },
            '/confidence-intervals': {
                'method': 'POST',
                'description': 'Calculate confidence intervals',
                'parameters': {
                    'interval_type': 'Type of interval (required)',
                    'confidence_level': 'Confidence level 0-1 (required)',
                    'decimals': 'Number of decimal places for rounding (default 4)'
                },
                'interval_types': {
                    'mean': 'Confidence interval for population mean',
                    'proportion': 'Confidence interval for population proportion',
                    'sample_size_mean': 'Required sample size for mean estimation',
                    'sample_size_proportion': 'Required sample size for proportion estimation'
                }
            },
            '/hypothesis-testing': {
                'method': 'POST',
                'description': 'Perform hypothesis testing',
                'parameters': {
                    'test_type': 'Type of test (required)',
                    'alpha': 'Significance level 0-1 (required)',
                    'tail_type': 'Type of test: two-tailed, left-tailed, right-tailed (required)',
                    'decimals': 'Number of decimal places for rounding (default 4)'
                },
                'test_types': {
                    'one_sample_mean': 'One-sample t-test or z-test for mean',
                    'one_sample_proportion': 'One-sample z-test for proportion',
                    'two_sample_mean': 'Two-sample t-test for difference in means',
                    'two_sample_proportion': 'Two-sample z-test for difference in proportions'
                }
            }
        },
        'general_notes': [
            'All endpoints return detailed step-by-step solutions',
            'Results include formulas, interpretations, and conclusions',
            'Use the decimals parameter to control output precision',
            'The rounded_display field shows values rounded to specified decimals'
        ]
    }
    
    return jsonify(help_info)