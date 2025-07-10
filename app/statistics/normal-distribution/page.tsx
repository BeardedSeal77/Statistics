// app/statistics/normal-distribution/page.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'

interface NormalResults {
  [key: string]: any
}

export default function NormalDistributionPage() {
  const [mean, setMean] = useState('')
  const [stdDev, setStdDev] = useState('')
  const [calculationType, setCalculationType] = useState('z_score')
  const [xValue, setXValue] = useState('')
  const [x1, setX1] = useState('')
  const [x2, setX2] = useState('')
  const [percentile, setPercentile] = useState('')
  const [confidenceLevel, setConfidenceLevel] = useState('')
  const [comparison, setComparison] = useState('less_than')
  const [decimals, setDecimals] = useState(4)
  const [results, setResults] = useState<NormalResults | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const calculationTypes = [
    { id: 'z_score', label: 'Z-Score Calculation', icon: '🎯' },
    { id: 'probability', label: 'Probability Calculation', icon: '📊' },
    { id: 'probability_between', label: 'Probability Between Values', icon: '📏' },
    { id: 'percentile', label: 'Find Percentile Value', icon: '📍' },
    { id: 'critical_values', label: 'Critical Values', icon: '⚡' },
    { id: 'empirical_rule', label: 'Empirical Rule (68-95-99.7)', icon: '📈' }
  ]

  const calculate = async () => {
    if (!mean || !stdDev) {
      setError('Please enter mean and standard deviation')
      return
    }

    setLoading(true)
    setError('')

    try {
      const requestData: any = {
        mean: parseFloat(mean),
        std_dev: parseFloat(stdDev),
        calculation_type: calculationType,
        decimals
      }

      // Add specific parameters based on calculation type
      if (calculationType === 'z_score' || calculationType === 'probability') {
        if (!xValue) {
          throw new Error('Please enter an x-value')
        }
        requestData.x_value = parseFloat(xValue)
        if (calculationType === 'probability') {
          requestData.comparison = comparison
        }
      } else if (calculationType === 'probability_between') {
        if (!x1 || !x2) {
          throw new Error('Please enter both x1 and x2 values')
        }
        requestData.x1 = parseFloat(x1)
        requestData.x2 = parseFloat(x2)
      } else if (calculationType === 'percentile') {
        if (!percentile) {
          throw new Error('Please enter a percentile value')
        }
        requestData.percentile = parseFloat(percentile)
      } else if (calculationType === 'critical_values') {
        if (!confidenceLevel) {
          throw new Error('Please enter a confidence level')
        }
        requestData.confidence_level = parseFloat(confidenceLevel) / 100
      }

      const response = await fetch('/api/statistics/normal-distribution', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })

      const result = await response.json()

      if (!result.success) {
        throw new Error(result.error || 'Failed to calculate')
      }

      setResults(result.results)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  const renderInputs = () => {
    switch (calculationType) {
      case 'z_score':
      case 'probability':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-subtle mb-2">
                X Value
              </label>
              <input
                type="number"
                step="any"
                value={xValue}
                onChange={(e) => setXValue(e.target.value)}
                placeholder="Enter x-value"
                className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
              />
            </div>
            {calculationType === 'probability' && (
              <div>
                <label className="block text-sm font-medium text-subtle mb-2">
                  Comparison Type
                </label>
                <select
                  value={comparison}
                  onChange={(e) => setComparison(e.target.value)}
                  className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text focus:border-gold focus:outline-none"
                >
                  <option value="less_than">P(X &lt; x)</option>
                  <option value="greater_than">P(X &gt; x)</option>
                  <option value="equal_to">P(X ≤ x)</option>
                </select>
              </div>
            )}
          </div>
        )
      
      case 'probability_between':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-subtle mb-2">
                Lower Bound (x₁)
              </label>
              <input
                type="number"
                step="any"
                value={x1}
                onChange={(e) => setX1(e.target.value)}
                placeholder="Enter lower bound"
                className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-subtle mb-2">
                Upper Bound (x₂)
              </label>
              <input
                type="number"
                step="any"
                value={x2}
                onChange={(e) => setX2(e.target.value)}
                placeholder="Enter upper bound"
                className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
              />
            </div>
          </div>
        )
      
      case 'percentile':
        return (
          <div>
            <label className="block text-sm font-medium text-subtle mb-2">
              Percentile (0-100)
            </label>
            <input
              type="number"
              min="0"
              max="100"
              step="0.1"
              value={percentile}
              onChange={(e) => setPercentile(e.target.value)}
              placeholder="e.g., 95"
              className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
            />
          </div>
        )
      
      case 'critical_values':
        return (
          <div>
            <label className="block text-sm font-medium text-subtle mb-2">
              Confidence Level (%)
            </label>
            <input
              type="number"
              min="80"
              max="99.9"
              step="0.1"
              value={confidenceLevel}
              onChange={(e) => setConfidenceLevel(e.target.value)}
              placeholder="e.g., 95"
              className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
            />
          </div>
        )
      
      default:
        return null
    }
  }

  const renderResults = () => {
    if (!results) return null

    return (
      <div className="bg-surface rounded-xl p-6 border border-muted">
        <h3 className="text-xl font-semibold text-text mb-6">Results</h3>
        
        {/* Main Result */}
        <div className="bg-gold/10 border border-gold rounded-lg p-4 mb-6">
          <div className="text-center">
            {calculationType === 'z_score' && (
              <div>
                <div className="text-3xl font-bold text-gold mb-2">
                  Z = {results.z_score?.toFixed(decimals)}
                </div>
                <div className="text-sm text-subtle">{results.interpretation}</div>
              </div>
            )}
            {calculationType === 'probability' && (
              <div>
                <div className="text-3xl font-bold text-gold mb-2">
                  P = {results.probability?.toFixed(decimals)}
                </div>
                <div className="text-lg text-subtle mb-1">
                  {(results.percentage)?.toFixed(2)}%
                </div>
                <div className="text-sm text-muted">Z = {results.z_score?.toFixed(decimals)}</div>
              </div>
            )}
            {calculationType === 'probability_between' && (
              <div>
                <div className="text-3xl font-bold text-gold mb-2">
                  P = {results.probability?.toFixed(decimals)}
                </div>
                <div className="text-lg text-subtle mb-1">
                  {(results.percentage)?.toFixed(2)}%
                </div>
                <div className="text-sm text-muted">
                  Z₁ = {results.z_scores?.[0]?.toFixed(decimals)}, Z₂ = {results.z_scores?.[1]?.toFixed(decimals)}
                </div>
              </div>
            )}
            {calculationType === 'percentile' && (
              <div>
                <div className="text-3xl font-bold text-gold mb-2">
                  X = {results.x_value?.toFixed(decimals)}
                </div>
                <div className="text-sm text-subtle">{results.interpretation}</div>
                <div className="text-sm text-muted">Z = {results.z_score?.toFixed(decimals)}</div>
              </div>
            )}
          </div>
        </div>

        {/* Formula */}
        {results.formula && (
          <div className="mb-4">
            <h4 className="font-semibold text-foam mb-2">Formula</h4>
            <div className="bg-base p-3 rounded font-mono text-sm border border-muted">
              {results.formula}
            </div>
          </div>
        )}

        {/* Steps */}
        {results.steps && (
          <div className="mb-4">
            <h4 className="font-semibold text-foam mb-2">Step-by-Step Solution</h4>
            <div className="space-y-2">
              {results.steps.map((step: string, index: number) => (
                <div key={index} className="bg-base p-2 rounded text-sm border border-muted font-mono">
                  {step}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empirical Rule Special Display */}
        {calculationType === 'empirical_rule' && results.one_std && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
              <div className="text-2xl font-bold text-foam mb-2">68%</div>
              <div className="text-sm text-subtle">Within 1σ</div>
              <div className="text-xs text-muted mt-1">
                [{results.one_std.lower.toFixed(decimals)}, {results.one_std.upper.toFixed(decimals)}]
              </div>
            </div>
            <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
              <div className="text-2xl font-bold text-rose mb-2">95%</div>
              <div className="text-sm text-subtle">Within 2σ</div>
              <div className="text-xs text-muted mt-1">
                [{results.two_std.lower.toFixed(decimals)}, {results.two_std.upper.toFixed(decimals)}]
              </div>
            </div>
            <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
              <div className="text-2xl font-bold text-iris mb-2">99.7%</div>
              <div className="text-sm text-subtle">Within 3σ</div>
              <div className="text-xs text-muted mt-1">
                [{results.three_std.lower.toFixed(decimals)}, {results.three_std.upper.toFixed(decimals)}]
              </div>
            </div>
          </div>
        )}

        {/* Critical Values Special Display */}
        {calculationType === 'critical_values' && results.x_critical_lower && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
              <div className="text-lg font-bold text-foam mb-1">Lower Critical Value</div>
              <div className="text-2xl font-bold text-text">{results.x_critical_lower.toFixed(decimals)}</div>
              <div className="text-sm text-muted">Z = {results.z_critical_lower.toFixed(decimals)}</div>
            </div>
            <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
              <div className="text-lg font-bold text-foam mb-1">Upper Critical Value</div>
              <div className="text-2xl font-bold text-text">{results.x_critical_upper.toFixed(decimals)}</div>
              <div className="text-sm text-muted">Z = {results.z_critical_upper.toFixed(decimals)}</div>
            </div>
          </div>
        )}

        {/* Description */}
        {results.description && (
          <div className="mt-4 p-3 bg-overlay rounded border border-muted">
            <div className="text-sm text-subtle">{results.description}</div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-base text-text">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/statistics" className="text-gold hover:text-yellow">
            ← Back to Statistics
          </Link>
          <h1 className="text-3xl font-bold text-gold">Normal Distribution Calculator</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Panel */}
          <div className="lg:col-span-1">
            <div className="bg-surface rounded-xl p-6 border border-muted sticky top-8">
              <h2 className="text-xl font-semibold text-text mb-6">Parameters</h2>
              
              {/* Distribution Parameters */}
              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-subtle mb-2">
                    Mean (μ)
                  </label>
                  <input
                    type="number"
                    step="any"
                    value={mean}
                    onChange={(e) => setMean(e.target.value)}
                    placeholder="e.g., 100"
                    className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-subtle mb-2">
                    Standard Deviation (σ)
                  </label>
                  <input
                    type="number"
                    step="any"
                    min="0.01"
                    value={stdDev}
                    onChange={(e) => setStdDev(e.target.value)}
                    placeholder="e.g., 15"
                    className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
                  />
                </div>
              </div>

              {/* Calculation Type */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-subtle mb-2">
                  Calculation Type
                </label>
                <select
                  value={calculationType}
                  onChange={(e) => setCalculationType(e.target.value)}
                  className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text focus:border-gold focus:outline-none"
                >
                  {calculationTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.icon} {type.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Dynamic Inputs */}
              <div className="mb-6">
                {renderInputs()}
              </div>

              {/* Decimal Places */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-subtle mb-2">
                  Decimal Places
                </label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={decimals}
                  onChange={(e) => setDecimals(parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text focus:border-gold focus:outline-none"
                />
              </div>

              {/* Calculate Button */}
              <button
                onClick={calculate}
                disabled={loading}
                className="w-full bg-gold hover:bg-yellow disabled:bg-muted text-base font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
              >
                {loading ? 'Calculating...' : 'Calculate'}
              </button>

              {/* Error Display */}
              {error && (
                <div className="mt-4 p-3 bg-red/20 border border-red rounded-lg text-red text-sm">
                  {error}
                </div>
              )}
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {results ? (
              renderResults()
            ) : (
              <div className="bg-surface rounded-xl p-12 border border-muted text-center">
                <div className="text-6xl mb-4">📈</div>
                <h3 className="text-xl font-semibold text-text mb-2">Normal Distribution Calculator</h3>
                <p className="text-subtle mb-8">
                  Enter your distribution parameters and select a calculation type to get detailed results with step-by-step explanations.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left max-w-2xl mx-auto">
                  <div className="bg-overlay p-4 rounded-lg border border-muted">
                    <h4 className="font-semibold text-foam mb-2">What you can calculate:</h4>
                    <ul className="text-sm text-subtle space-y-1">
                      <li>• Z-scores for any value</li>
                      <li>• Probabilities and percentages</li>
                      <li>• Critical values for confidence intervals</li>
                      <li>• Empirical rule boundaries</li>
                    </ul>
                  </div>
                  <div className="bg-overlay p-4 rounded-lg border border-muted">
                    <h4 className="font-semibold text-foam mb-2">Example use cases:</h4>
                    <ul className="text-sm text-subtle space-y-1">
                      <li>• Test scores: μ=75, σ=10</li>
                      <li>• Heights: μ=170, σ=8</li>
                      <li>• IQ scores: μ=100, σ=15</li>
                      <li>• Manufacturing tolerances</li>
                    </ul>
                  </div>
                </div>

                <div className="mt-8">
                  <button
                    onClick={() => {
                      setMean('100')
                      setStdDev('15')
                      setXValue('115')
                      setCalculationType('z_score')
                    }}
                    className="bg-overlay hover:bg-highlight-med text-text px-4 py-2 rounded border border-muted transition-colors"
                  >
                    Try Example: IQ Score Z-Score
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}