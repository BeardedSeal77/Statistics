# Statistics Website Project Structure

## Backend Structure (Flask)

```
api/
├── __init__.py
├── index.py (main Flask app)
├── statistics/
│   ├── __init__.py
│   ├── descriptive_stats.py
│   ├── normal_distribution.py
│   ├── confidence_intervals.py
│   ├── hypothesis_testing.py
│   └── utils.py
└── routes/
    ├── __init__.py
    └── stats_routes.py
```

## Frontend Structure (Next.js)

```
app/
├── statistics/
│   ├── layout.tsx
│   ├── page.tsx (main stats dashboard)
│   ├── descriptive/
│   │   └── page.tsx
│   ├── normal-distribution/
│   │   └── page.tsx
│   ├── confidence-intervals/
│   │   └── page.tsx
│   └── hypothesis-testing/
│       ├── page.tsx
│       ├── one-sample-mean/
│       │   └── page.tsx
│       ├── one-sample-proportion/
│       │   └── page.tsx
│       ├── two-sample-mean/
│       │   └── page.tsx
│       └── two-sample-proportion/
│           └── page.tsx
├── components/
│   ├── statistics/
│   │   ├── StatsCard.tsx
│   │   ├── StatsForm.tsx
│   │   ├── StatsResults.tsx
│   │   ├── StepByStep.tsx
│   │   └── FormulaDisplay.tsx
│   └── ui/
│       ├── Input.tsx
│       ├── Button.tsx
│       └── Card.tsx
└── globals.css
```

## Key Features Implementation

### 1. Python Statistics Classes
- **DescriptiveStats**: Handles mean, median, mode, variance, std dev, percentiles
- **NormalDistribution**: Z-scores, probabilities, critical values
- **ConfidenceIntervals**: Mean and proportion confidence intervals
- **HypothesisTesting**: One and two sample tests for means and proportions

### 2. API Endpoints
- `POST /api/statistics/descriptive` - Calculate descriptive statistics
- `POST /api/statistics/normal-distribution` - Normal distribution calculations
- `POST /api/statistics/confidence-intervals` - CI calculations
- `POST /api/statistics/hypothesis-testing` - Hypothesis tests

### 3. Frontend Components
- **StatsCard**: Display individual statistics
- **StatsForm**: Input forms for different analysis types
- **StatsResults**: Show results with step-by-step explanations
- **StepByStep**: Display calculation steps and formulas
- **FormulaDisplay**: Render mathematical formulas

### 4. User Interface Features
- Question type selection
- Dynamic input forms based on selected analysis
- Decimal places control for rounding
- Step-by-step solution display
- Formula explanations
- Results export functionality

### 5. Data Flow
1. User selects analysis type
2. Form renders with appropriate inputs
3. Data sent to Flask backend
4. Python classes perform calculations
5. Results returned with steps and explanations
6. Frontend displays formatted results

## Installation & Setup

1. **Backend Dependencies**:
   ```bash
   pip install flask scipy numpy pandas
   ```

2. **Frontend Dependencies**:
   ```bash
   npm install recharts react-katex katex
   ```

3. **Run Development Server**:
   ```bash
   npm run dev
   ```

This structure provides a scalable foundation for statistical analysis with clear separation of concerns and comprehensive coverage of statistical methods.