"""
Display helper functions for the Statistics Calculator Console Application
Handles output formatting and display utilities.
"""

from typing import Dict, Any, List, Union
import textwrap


def format_number(value: Union[int, float], decimal_places: int = 4) -> str:
    """Format a number with specified decimal places"""
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        else:
            return f"{value:.{decimal_places}f}"
    else:
        return str(value)


def format_list(values: List[Union[int, float]], decimal_places: int = 4) -> str:
    """Format a list of numbers"""
    formatted = [format_number(v, decimal_places) for v in values]
    return f"[{', '.join(formatted)}]"


def print_section_header(title: str, width: int = 50):
    """Print a formatted section header"""
    print(f"\n{title}")
    print("=" * len(title))


def print_subsection_header(title: str):
    """Print a formatted subsection header"""
    print(f"\n{title}")
    print("-" * len(title))


def print_result(name: str, value: Any, decimal_places: int = 4, description: str = None):
    """Print a formatted result with optional description"""
    if isinstance(value, (int, float)):
        exact_str = str(value)
        rounded_str = format_number(value, decimal_places)
        
        if exact_str == rounded_str:
            print(f"   {name}: {exact_str}")
        else:
            print(f"   {name}: {exact_str} (rounded: {rounded_str})")
    else:
        print(f"   {name}: {value}")
    
    if description:
        wrapped_desc = textwrap.fill(description, width=70, initial_indent="      ", subsequent_indent="      ")
        print(wrapped_desc)


def print_formula(formula: str):
    """Print a formatted formula"""
    print(f"\n📐 Formula: {formula}")


def print_steps(steps: List[str], title: str = "Step-by-Step Solution"):
    """Print formatted calculation steps"""
    print(f"\n📝 {title}:")
    for i, step in enumerate(steps, 1):
        # Wrap long steps
        wrapped_step = textwrap.fill(step, width=70, initial_indent=f"   {i}. ", subsequent_indent="      ")
        print(wrapped_step)


def print_interpretation(interpretation: str):
    """Print formatted interpretation"""
    wrapped = textwrap.fill(interpretation, width=70, initial_indent="💡 ", subsequent_indent="   ")
    print(f"\n{wrapped}")


def print_warning(warning: str):
    """Print formatted warning"""
    wrapped = textwrap.fill(warning, width=70, initial_indent="⚠️  ", subsequent_indent="   ")
    print(f"\n{wrapped}")


def print_conclusion(conclusion: str):
    """Print formatted conclusion"""
    wrapped = textwrap.fill(conclusion, width=70, initial_indent="✅ ", subsequent_indent="   ")
    print(f"\n{wrapped}")


def print_confidence_interval(lower: float, upper: float, confidence_level: float, decimal_places: int = 4):
    """Print a formatted confidence interval"""
    lower_str = format_number(lower, decimal_places)
    upper_str = format_number(upper, decimal_places)
    confidence_pct = confidence_level * 100
    print(f"\n🎯 {confidence_pct}% Confidence Interval: [{lower_str}, {upper_str}]")


def print_hypothesis_decision(reject_null: bool, conclusion: str):
    """Print hypothesis test decision"""
    decision = "REJECT" if reject_null else "FAIL TO REJECT"
    emoji = "❌" if reject_null else "✅"
    print(f"\n{emoji} Decision: {decision} the null hypothesis")
    print(f"   Conclusion: {conclusion}")


def print_data_summary(data: List[float], decimal_places: int = 4):
    """Print a summary of the dataset"""
    print(f"\n📊 Data Summary:")
    print(f"   Sample Size: {len(data)}")
    print(f"   Data: {format_list(data, decimal_places)}")
    print(f"   Min: {format_number(min(data), decimal_places)}")
    print(f"   Max: {format_number(max(data), decimal_places)}")


def print_table(headers: List[str], rows: List[List[str]], title: str = None):
    """Print a formatted table"""
    if title:
        print(f"\n{title}")
    
    # Calculate column widths
    widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Print headers
    header_row = " | ".join(header.ljust(widths[i]) for i, header in enumerate(headers))
    print(f"   {header_row}")
    print(f"   {'-' * len(header_row)}")
    
    # Print rows
    for row in rows:
        data_row = " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
        print(f"   {data_row}")


def print_five_number_summary(minimum: float, q1: float, median: float, q3: float, maximum: float, decimal_places: int = 4):
    """Print the five-number summary in a formatted way"""
    print(f"\n📊 Five-Number Summary:")
    print(f"   Minimum: {format_number(minimum, decimal_places)}")
    print(f"   Q1:      {format_number(q1, decimal_places)}")
    print(f"   Median:  {format_number(median, decimal_places)}")
    print(f"   Q3:      {format_number(q3, decimal_places)}")
    print(f"   Maximum: {format_number(maximum, decimal_places)}")


def print_empirical_rule(one_std: Dict, two_std: Dict, three_std: Dict, decimal_places: int = 4):
    """Print empirical rule results"""
    print(f"\n📈 Empirical Rule (68-95-99.7):")
    
    one_lower = format_number(one_std['lower'], decimal_places)
    one_upper = format_number(one_std['upper'], decimal_places)
    print(f"   68% of data within 1σ: [{one_lower}, {one_upper}]")
    
    two_lower = format_number(two_std['lower'], decimal_places)
    two_upper = format_number(two_std['upper'], decimal_places)
    print(f"   95% of data within 2σ: [{two_lower}, {two_upper}]")
    
    three_lower = format_number(three_std['lower'], decimal_places)
    three_upper = format_number(three_std['upper'], decimal_places)
    print(f"   99.7% of data within 3σ: [{three_lower}, {three_upper}]")


def create_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Create a simple progress bar string"""
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)
    return f"[{bar}] {percentage}%"


def print_menu_option(number: int, description: str, emoji: str = ""):
    """Print a formatted menu option"""
    emoji_str = f"{emoji} " if emoji else ""
    print(f"{number}. {emoji_str}{description}")


def clear_lines(n: int = 1):
    """Clear n lines from the console"""
    for _ in range(n):
        print("\033[A\033[K", end="")


def print_divider(char: str = "-", length: int = 50):
    """Print a divider line"""
    print(char * length)


def print_box(text: str, padding: int = 2):
    """Print text in a box"""
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    width = max_length + 2 * padding
    
    print("+" + "-" * width + "+")
    for line in lines:
        padded_line = line.center(width)
        print(f"|{padded_line}|")
    print("+" + "-" * width + "+")


def format_scientific(value: float, decimal_places: int = 4) -> str:
    """Format very small or large numbers in scientific notation when appropriate"""
    if abs(value) < 0.001 or abs(value) > 1000000:
        return f"{value:.{decimal_places}e}"
    else:
        return format_number(value, decimal_places)