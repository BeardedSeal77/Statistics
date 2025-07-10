// app/statistics/descriptive/page.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'

interface DescriptiveResults {
  data_info: {
    original_data: number[]
    sorted_data: number[]
    sample_size: number
  }
  measures_of_central_tendency: any
  measures_of_dispersion: any
  measures_of_position: any
  distribution_shape: any
  five_number_summary: any
  custom_percentile?: any
  standard_error_analysis?: any
}

export default function DescriptiveStatsPage() {
  const [dataInput, setDataInput] = useState('')
  const [customPercentile, setCustomPercentile] = useState('')
  const [includeStandardError, setIncludeStandardError] = useState(false)
  const [confidenceLevel, setConfidenceLevel] = useState(95)
  const [decimals, setDecimals] = useState(4)
  const [results, setResults] = useState<DescriptiveResults | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('central')

  const calculateStats = async () => {
    if (!dataInput.trim()) {
      setError('Please enter some data')
      return
    }

    setLoading(true)
    setError('')

    try {
      // Parse the data input - handle various formats
      const data = dataInput
        .split(/[,\s\n]+/)
        .filter(val => val.trim() !== '')
        .map(val => {
          const num = parseFloat(val.trim())
          if (isNaN(num)) throw new Error(`Invalid number: ${val}`)
          return num
        })

      if (data.length < 2) {
        throw new Error('Please enter at least 2 numbers')
      }

      const requestData = {
        data,
        custom_percentile: customPercentile ? parseFloat(customPercentile) : null,
        include_standard_error: includeStandardError,
        confidence_level: confidenceLevel / 100,
        decimals
      }

      const response = await fetch('/api/statistics/descriptive', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })

      const result = await response.json()

      if (!result.success) {
        throw new Error(result.error || 'Failed to calculate statistics')
      }

      setResults(result.results)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  const StatCard = ({ title, value, formula, description, steps }: any) => (
    <div className="bg-overlay rounded-lg p-4 border border-muted">
      <h4 className="font-semibold text-foam mb-2">{title}</h4>
      <div className="text-2xl font-bold text-text mb-2">
        {typeof value === 'number' ? value.toFixed(decimals) : value || 'N/A'}
      </div>
      {formula && (
        <div className="text-xs text-muted mb-2 font-mono bg-base p-2 rounded">
          {formula}
        </div>
      )}
      {description && (
        <p className="text-sm text-subtle mb-3">{description}</p>
      )}
      {steps && (
        <details className="text-xs">
          <summary className="cursor-pointer text-gold hover:text-yellow">
            Show calculation steps
          </summary>
          <div className="mt-2 space-y-1 text-subtle">
            {steps.map((step: string, index: number) => (
              <div key={index} className="font-mono bg-base p-1 rounded">
                {step}
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  )

  const tabs = [
    { id: 'central', label: 'Central Tendency', icon: '📊' },
    { id: 'dispersion', label: 'Dispersion', icon: '📏' },
    { id: 'position', label: 'Position', icon: '📍' },
    { id: 'shape', label: 'Shape', icon: '📈' },
    { id: 'summary', label: 'Summary', icon: '📋' }
  ]

  return (
    <div className="min-h-screen bg-base text-text">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/statistics" className="text-gold hover:text-yellow">
            ← Back to Statistics
          </Link>
          <h1 className="text-3xl font-bold text-gold">Descriptive Statistics Calculator</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Panel */}
          <div className="lg:col-span-1">
            <div className="bg-surface rounded-xl p-6 border border-muted sticky top-8">
              <h2 className="text-xl font-semibold text-text mb-6">Input Data</h2>
              
              {/* Data Input */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-subtle mb-2">
                  Dataset (comma or space separated)
                </label>
                <textarea
                  value={dataInput}
                  onChange={(e) => setDataInput(e.target.value)}
                  placeholder="Enter your data: 1, 2, 3, 4, 5 or 1 2 3 4 5"
                  className="w-full h-32 px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
                />
              </div>

              {/* Custom Percentile */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-subtle mb-2">
                  Custom Percentile (optional)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.1"
                  value={customPercentile}
                  onChange={(e) => setCustomPercentile(e.target.value)}
                  placeholder="e.g., 75"
                  className="w-full px-3 py-2 bg-base border border-muted rounded-lg text-text placeholder-muted focus:border-gold focus:outline-none"
                />
              </div>

              {/* Standard Error Analysis */}
              <div className="mb-4">
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={includeStandardError}
                    onChange={(e) => setIncludeStandardError(e.target.checked)}
                    className="rounded border-muted"
                  />
                  <span className="text-subtle">Include Standard Error Analysis</span>
                </label>
                {includeStandardError && (
                  <div className="mt-2">
                    <label className="block text-xs text-muted mb-1">
                      Confidence Level (%)
                    </label>
                    <input
                      type="number"
                      min="80"
                      max="99.9"
                      step="0.1"
                      value={confidenceLevel}
                      onChange={(e) => setConfidenceLevel(parseFloat(e.target.value))}
                      className="w-full px-2 py-1 bg-base border border-muted rounded text-sm"
                    />
                  </div>
                )}
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
                onClick={calculateStats}
                disabled={loading}
                className="w-full bg-gold hover:bg-yellow disabled:bg-muted text-base font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
              >
                {loading ? 'Calculating...' : 'Calculate Statistics'}
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
              <div>
                {/* Data Info */}
                <div className="bg-surface rounded-xl p-6 border border-muted mb-6">
                  <h2 className="text-xl font-semibold text-text mb-4">Data Summary</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-foam">{results.data_info.sample_size}</div>
                      <div className="text-sm text-subtle">Sample Size</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg text-subtle">Original Data</div>
                      <div className="text-xs text-muted bg-base p-2 rounded mt-1 max-h-20 overflow-auto">
                        [{results.data_info.original_data.join(', ')}]
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg text-subtle">Sorted Data</div>
                      <div className="text-xs text-muted bg-base p-2 rounded mt-1 max-h-20 overflow-auto">
                        [{results.data_info.sorted_data.join(', ')}]
                      </div>
                    </div>
                  </div>
                </div>

                {/* Tab Navigation */}
                <div className="flex flex-wrap gap-2 mb-6">
                  {tabs.map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        activeTab === tab.id
                          ? 'bg-gold text-base'
                          : 'bg-surface text-subtle hover:text-text border border-muted'
                      }`}
                    >
                      {tab.icon} {tab.label}
                    </button>
                  ))}
                </div>

                {/* Tab Content */}
                <div className="bg-surface rounded-xl p-6 border border-muted">
                  {activeTab === 'central' && (
                    <div>
                      <h3 className="text-lg font-semibold text-text mb-4">Measures of Central Tendency</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <StatCard
                          title="Mean"
                          value={results.measures_of_central_tendency.mean.value}
                          formula={results.measures_of_central_tendency.mean.formula}
                          description={results.measures_of_central_tendency.mean.description}
                          steps={results.measures_of_central_tendency.mean.steps}
                        />
                        <StatCard
                          title="Median"
                          value={results.measures_of_central_tendency.median.value}
                          formula={results.measures_of_central_tendency.median.formula}
                          description={results.measures_of_central_tendency.median.description}
                          steps={results.measures_of_central_tendency.median.steps}
                        />
                        <StatCard
                          title="Mode"
                          value={results.measures_of_central_tendency.mode.value}
                          formula={results.measures_of_central_tendency.mode.formula}
                          description={results.measures_of_central_tendency.mode.description}
                          steps={results.measures_of_central_tendency.mode.steps}
                        />
                      </div>
                    </div>
                  )}

                  {activeTab === 'dispersion' && (
                    <div>
                      <h3 className="text-lg font-semibold text-text mb-4">Measures of Dispersion</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <StatCard
                          title="Sample Variance"
                          value={results.measures_of_dispersion.sample_variance.value}
                          formula={results.measures_of_dispersion.sample_variance.formula}
                          description={results.measures_of_dispersion.sample_variance.description}
                          steps={results.measures_of_dispersion.sample_variance.steps}
                        />
                        <StatCard
                          title="Sample Standard Deviation"
                          value={results.measures_of_dispersion.sample_std_dev.value}
                          formula={results.measures_of_dispersion.sample_std_dev.formula}
                          description={results.measures_of_dispersion.sample_std_dev.description}
                          steps={results.measures_of_dispersion.sample_std_dev.steps}
                        />
                        <StatCard
                          title="Population Variance"
                          value={results.measures_of_dispersion.population_variance.value}
                          formula={results.measures_of_dispersion.population_variance.formula}
                          description={results.measures_of_dispersion.population_variance.description}
                          steps={results.measures_of_dispersion.population_variance.steps}
                        />
                        <StatCard
                          title="Range"
                          value={results.measures_of_dispersion.range.value}
                          formula={results.measures_of_dispersion.range.formula}
                          description={results.measures_of_dispersion.range.description}
                          steps={results.measures_of_dispersion.range.steps}
                        />
                      </div>
                    </div>
                  )}

                  {activeTab === 'position' && (
                    <div>
                      <h3 className="text-lg font-semibold text-text mb-4">Measures of Position</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <StatCard
                          title="Q1 (25th Percentile)"
                          value={results.measures_of_position.q1.value}
                          formula={results.measures_of_position.q1.formula}
                          description={results.measures_of_position.q1.description}
                          steps={results.measures_of_position.q1.steps}
                        />
                        <StatCard
                          title="Q2 (50th Percentile)"
                          value={results.measures_of_position.q2.value}
                          formula={results.measures_of_position.q2.formula}
                          description={results.measures_of_position.q2.description}
                          steps={results.measures_of_position.q2.steps}
                        />
                        <StatCard
                          title="Q3 (75th Percentile)"
                          value={results.measures_of_position.q3.value}
                          formula={results.measures_of_position.q3.formula}
                          description={results.measures_of_position.q3.description}
                          steps={results.measures_of_position.q3.steps}
                        />
                      </div>
                      {results.custom_percentile && (
                        <div className="mt-4">
                          <StatCard
                            title={`Custom ${results.custom_percentile.percentile}th Percentile`}
                            value={results.custom_percentile.value}
                            formula={results.custom_percentile.formula}
                            description={results.custom_percentile.description}
                            steps={results.custom_percentile.steps}
                          />
                        </div>
                      )}
                    </div>
                  )}

                  {activeTab === 'shape' && (
                    <div>
                      <h3 className="text-lg font-semibold text-text mb-4">Distribution Shape</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-overlay rounded-lg p-4 border border-muted">
                          <h4 className="font-semibold text-foam mb-2">Skewness</h4>
                          <div className="text-2xl font-bold text-text mb-2">
                            {results.distribution_shape.skewness.value.toFixed(decimals)}
                          </div>
                          <div className="text-sm text-subtle mb-2">
                            {results.distribution_shape.skewness.interpretation}
                          </div>
                          <div className="text-xs text-muted font-mono bg-base p-2 rounded">
                            {results.distribution_shape.skewness.formula}
                          </div>
                          <p className="text-sm text-subtle mt-2">
                            {results.distribution_shape.skewness.description}
                          </p>
                        </div>
                        <div className="bg-overlay rounded-lg p-4 border border-muted">
                          <h4 className="font-semibold text-foam mb-2">Kurtosis</h4>
                          <div className="text-2xl font-bold text-text mb-2">
                            {results.distribution_shape.kurtosis.value.toFixed(decimals)}
                          </div>
                          <div className="text-sm text-subtle mb-2">
                            {results.distribution_shape.kurtosis.interpretation}
                          </div>
                          <div className="text-xs text-muted font-mono bg-base p-2 rounded">
                            {results.distribution_shape.kurtosis.formula}
                          </div>
                          <p className="text-sm text-subtle mt-2">
                            {results.distribution_shape.kurtosis.description}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'summary' && (
                    <div>
                      <h3 className="text-lg font-semibold text-text mb-4">Five-Number Summary</h3>
                      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
                        <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
                          <div className="text-lg font-bold text-text">{results.five_number_summary.minimum}</div>
                          <div className="text-sm text-subtle">Minimum</div>
                        </div>
                        <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
                          <div className="text-lg font-bold text-text">{results.five_number_summary.q1}</div>
                          <div className="text-sm text-subtle">Q1</div>
                        </div>
                        <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
                          <div className="text-lg font-bold text-text">{results.five_number_summary.median}</div>
                          <div className="text-sm text-subtle">Median</div>
                        </div>
                        <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
                          <div className="text-lg font-bold text-text">{results.five_number_summary.q3}</div>
                          <div className="text-sm text-subtle">Q3</div>
                        </div>
                        <div className="bg-overlay rounded-lg p-4 border border-muted text-center">
                          <div className="text-lg font-bold text-text">{results.five_number_summary.maximum}</div>
                          <div className="text-sm text-subtle">Maximum</div>
                        </div>
                      </div>
                      <StatCard
                        title="Interquartile Range (IQR)"
                        value={results.five_number_summary.iqr.value}
                        formula={results.five_number_summary.iqr.formula}
                        description={results.five_number_summary.iqr.description}
                        steps={results.five_number_summary.iqr.steps}
                      />
                      
                      {results.standard_error_analysis && (
                        <div className="mt-6">
                          <h4 className="text-lg font-semibold text-text mb-4">Standard Error Analysis</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <StatCard
                              title="Standard Error"
                              value={results.standard_error_analysis.standard_error.value}
                              formula={results.standard_error_analysis.standard_error.formula}
                              description={results.standard_error_analysis.standard_error.description}
                              steps={results.standard_error_analysis.standard_error.steps}
                            />
                            <StatCard
                              title="Margin of Error"
                              value={results.standard_error_analysis.margin_of_error.value}
                              formula={results.standard_error_analysis.margin_of_error.formula}
                              description={results.standard_error_analysis.margin_of_error.description}
                              steps={results.standard_error_analysis.margin_of_error.steps}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-surface rounded-xl p-12 border border-muted text-center">
                <div className="text-6xl mb-4">📊</div>
                <h3 className="text-xl font-semibold text-text mb-2">Ready to Calculate</h3>
                <p className="text-subtle">Enter your dataset and click "Calculate Statistics" to see comprehensive results with step-by-step explanations.</p>
                
                <div className="mt-8 text-left max-w-md mx-auto">
                  <h4 className="font-semibold text-text mb-3">Example datasets to try:</h4>
                  <div className="space-y-2 text-sm">
                    <button
                      onClick={() => setDataInput('12, 15, 18, 21, 24, 27, 30')}
                      className="block w-full text-left p-2 bg-overlay rounded border border-muted hover:border-gold transition-colors"
                    >
                      <strong>Simple:</strong> 12, 15, 18, 21, 24, 27, 30
                    </button>
                    <button
                      onClick={() => setDataInput('85, 92, 78, 96, 87, 91, 89, 93, 88, 94')}
                      className="block w-full text-left p-2 bg-overlay rounded border border-muted hover:border-gold transition-colors"
                    >
                      <strong>Test Scores:</strong> 85, 92, 78, 96, 87, 91, 89, 93, 88, 94
                    </button>
                    <button
                      onClick={() => setDataInput('2.5, 3.1, 2.8, 3.4, 2.9, 3.2, 2.7, 3.0, 2.6, 3.3')}
                      className="block w-full text-left p-2 bg-overlay rounded border border-muted hover:border-gold transition-colors"
                    >
                      <strong>Decimal:</strong> 2.5, 3.1, 2.8, 3.4, 2.9, 3.2, 2.7, 3.0, 2.6, 3.3
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}