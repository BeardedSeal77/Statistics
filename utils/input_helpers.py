"""
Input helper functions for the Statistics Calculator Console Application
Handles user input validation and data collection.
"""

from typing import List, Optional, Union


def get_float(prompt: str, default: Optional[float] = None) -> float:
    """Get a float from user input with validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                return default
            return float(user_input)
        except ValueError:
            print("❌ Please enter a valid number.")


def get_positive_float(prompt: str) -> float:
    """Get a positive float from user input"""
    while True:
        value = get_float(prompt)
        if value > 0:
            return value
        print("❌ Please enter a positive number.")


def get_int(prompt: str, default: Optional[int] = None) -> int:
    """Get an integer from user input with validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                return default
            return int(user_input)
        except ValueError:
            print("❌ Please enter a valid integer.")


def get_positive_int(prompt: str) -> int:
    """Get a positive integer from user input"""
    while True:
        value = get_int(prompt)
        if value > 0:
            return value
        print("❌ Please enter a positive integer.")


def get_int_in_range(prompt: str, min_val: int, max_val: int) -> Optional[int]:
    """Get an integer within a specific range"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                return None
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"❌ Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("❌ Please enter a valid integer.")


def get_proportion(prompt: str) -> float:
    """Get a proportion (value between 0 and 1) from user input"""
    while True:
        value = get_float(prompt)
        if 0 <= value <= 1:
            return value
        print("❌ Proportion must be between 0 and 1.")


def get_percentile() -> float:
    """Get a percentile value (0-100) from user input"""
    while True:
        value = get_float("Enter percentile (0-100): ")
        if 0 < value < 100:
            return value
        print("❌ Percentile must be between 0 and 100 (exclusive).")


def get_confidence_level() -> float:
    """Get a confidence level from user input"""
    print("\nCommon confidence levels:")
    print("  90% = 0.90")
    print("  95% = 0.95")
    print("  99% = 0.99")
    
    while True:
        value = get_float("Enter confidence level (0-1): ")
        if 0 < value < 1:
            return value
        print("❌ Confidence level must be between 0 and 1.")


def get_alpha() -> float:
    """Get significance level (alpha) from user input"""
    print("\nCommon significance levels:")
    print("  α = 0.01 (99% confidence)")
    print("  α = 0.05 (95% confidence)")
    print("  α = 0.10 (90% confidence)")
    
    while True:
        value = get_float("Enter significance level α (0-1): ")
        if 0 < value < 1:
            return value
        print("❌ Significance level must be between 0 and 1.")


def get_yes_no(prompt: str) -> bool:
    """Get a yes/no response from user"""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes', '1', 'true']:
            return True
        elif response in ['n', 'no', '0', 'false']:
            return False
        print("❌ Please enter 'y' for yes or 'n' for no.")


def get_dataset() -> List[float]:
    """Get a dataset from user input"""
    print("\nEnter your dataset:")
    print("You can enter numbers in several ways:")
    print("  - Space separated: 1 2 3 4 5")
    print("  - Comma separated: 1, 2, 3, 4, 5")
    print("  - One per line (press Enter twice when done)")
    
    # Try single line input first
    single_line = input("\nEnter data (single line): ").strip()
    
    if single_line:
        # Parse single line input
        try:
            # Try comma separated first
            if ',' in single_line:
                numbers = [float(x.strip()) for x in single_line.split(',') if x.strip()]
            else:
                # Try space separated
                numbers = [float(x.strip()) for x in single_line.split() if x.strip()]
            
            if len(numbers) >= 2:
                print(f"✅ Dataset loaded: {numbers}")
                return numbers
            else:
                print("❌ Please enter at least 2 numbers.")
                
        except ValueError:
            print("❌ Error parsing numbers. Please check your input.")
    
    # Multi-line input as fallback
    print("\nEnter numbers one per line (press Enter on empty line when done):")
    numbers = []
    while True:
        try:
            line = input("Number: ").strip()
            if not line:  # Empty line means done
                break
            numbers.append(float(line))
        except ValueError:
            print("❌ Please enter a valid number.")
    
    if len(numbers) >= 2:
        print(f"✅ Dataset loaded: {numbers}")
        return numbers
    else:
        print("❌ Please enter at least 2 numbers.")
        return get_dataset()  # Try again


def get_custom_percentile() -> Optional[float]:
    """Get an optional custom percentile from user"""
    if get_yes_no("Calculate a custom percentile? (y/n): "):
        return get_percentile()
    return None


def get_comparison_type() -> str:
    """Get comparison type for probability calculations"""
    print("\nSelect comparison type:")
    print("1. P(X < x) - Less than")
    print("2. P(X > x) - Greater than") 
    print("3. P(X ≤ x) - Less than or equal")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            return 'less_than'
        elif choice == '2':
            return 'greater_than'
        elif choice == '3':
            return 'equal_to'
        else:
            print("❌ Please enter 1, 2, or 3.")


def get_tail_type() -> str:
    """Get tail type for hypothesis testing"""
    print("\nSelect test type:")
    print("1. Two-tailed test (≠)")
    print("2. Left-tailed test (<)")
    print("3. Right-tailed test (>)")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            return 'two-tailed'
        elif choice == '2':
            return 'left-tailed'
        elif choice == '3':
            return 'right-tailed'
        else:
            print("❌ Please enter 1, 2, or 3.")


def confirm_data(data: List[float]) -> bool:
    """Ask user to confirm their data"""
    print(f"\nYour data: {data}")
    print(f"Count: {len(data)} values")
    return get_yes_no("Is this correct? (y/n): ")


def get_retry() -> bool:
    """Ask if user wants to retry"""
    return get_yes_no("Would you like to try again? (y/n): ")