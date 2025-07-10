// app/statistics/page.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'

interface StatModule {
  id: string
  title: string
  description: string
  icon: string
  href: string
  features: string[]
}

const statisticsModules: StatModule[] = [
  {
    id: 'descriptive',
    title: 'Descriptive Statistics',
    description: 'Calculate comprehensive descriptive statistics for your dataset',
    icon: '📊',
    href: '/statistics/descriptive',
    features: [
      'Mean, Median, Mode',
      'Variance & Standard Deviation',
      'Percentiles & Quartiles',
      'Skewness & Kurtosis',
      'Five-Number Summary',
      'Custom Percentiles'
    ]
  },
  {
    id: 'normal',
    title: 'Normal Distribution',
    description: 'Work with normal distributions and standardized scores',
    icon: '📈',
    href: '/statistics/normal-distribution',
    features: [
      'Z-Score Calculations',
      'Probability Calculations',
      'Percentile Finding',
      'Critical Values',
      'Empirical Rule (68-95-99.7)',
      'Between Probabilities'
    ]
  },
  {
    id: 'confidence',
    title: 'Confidence Intervals',
    description: 'Calculate confidence intervals for means and proportions',
    icon: '🎯',
    href: '/statistics/confidence-intervals',
    features: [
      'Mean Confidence Intervals',
      'Proportion Confidence Intervals',
      'Sample Size Determination',
      'Margin of Error Analysis',
      'Z & T Distributions',
      'Detailed Step Solutions'
    ]
  },
  {
    id: 'hypothesis',
    title: 'Hypothesis Testing',
    description: 'Perform comprehensive hypothesis tests with step-by-step solutions',
    icon: '🔬',
    href: '/statistics/hypothesis-testing',
    features: [
      'One & Two Sample Mean Tests',
      'One & Two Sample Proportion Tests',
      'Z-Tests & T-Tests',
      'P-Value Calculations',
      'Critical Value Method',
      'Effect Size Analysis'
    ]
  }
]

export default function StatisticsHome() {
  const [selectedModule, setSelectedModule] = useState<string | null>(null)

  return (
    <div className="min-h-screen bg-base text-text">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gold mb-4">
            Statistics Calculator Suite
          </h1>
          <p className="text-lg text-subtle max-w-3xl mx-auto">
            Comprehensive statistical analysis tools with detailed step-by-step solutions. 
            Perfect for students, researchers, and professionals who need accurate calculations 
            with complete explanations.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-surface rounded-lg p-6 text-center border border-muted">
            <div className="text-2xl font-bold text-foam">25+</div>
            <div className="text-sm text-subtle">Statistical Functions</div>
          </div>
          <div className="bg-surface rounded-lg p-6 text-center border border-muted">
            <div className="text-2xl font-bold text-rose">100%</div>
            <div className="text-sm text-subtle">Step-by-Step Solutions</div>
          </div>
          <div className="bg-surface rounded-lg p-6 text-center border border-muted">
            <div className="text-2xl font-bold text-iris">∞</div>
            <div className="text-sm text-subtle">Decimal Precision</div>
          </div>
          <div className="bg-surface rounded-lg p-6 text-center border border-muted">
            <div className="text-2xl font-bold text-pine">4</div>
            <div className="text-sm text-subtle">Major Categories</div>
          </div>
        </div>

        {/* Module Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {statisticsModules.map((module) => (
            <div
              key={module.id}
              className={`bg-surface rounded-xl p-8 border transition-all duration-300 hover:scale-105 cursor-pointer ${
                selectedModule === module.id 
                  ? 'border-gold shadow-lg shadow-gold/20' 
                  : 'border-muted hover:border-subtle'
              }`}
              onMouseEnter={() => setSelectedModule(module.id)}
              onMouseLeave={() => setSelectedModule(null)}
            >
              <div className="flex items-start gap-4 mb-6">
                <div className="text-4xl">{module.icon}</div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-text mb-2">
                    {module.title}
                  </h3>
                  <p className="text-subtle">
                    {module.description}
                  </p>
                </div>
              </div>

              {/* Features List */}
              <div className="mb-6">
                <h4 className="text-sm font-semibold text-muted mb-3 uppercase tracking-wide">
                  Features Include:
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {module.features.map((feature, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm">
                      <div className="w-1.5 h-1.5 bg-gold rounded-full"></div>
                      <span className="text-subtle">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Button */}
              <Link href={module.href}>
                <button className="w-full bg-gold hover:bg-yellow text-base font-semibold py-3 px-6 rounded-lg transition-colors duration-200">
                  Open Calculator
                </button>
              </Link>
            </div>
          ))}
        </div>

        {/* Additional Info */}
        <div className="mt-16 bg-overlay rounded-xl p-8 border border-muted">
          <h2 className="text-2xl font-bold text-text mb-4">Why Use Our Statistics Suite?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-foam mb-2">📚 Educational</h3>
              <p className="text-subtle text-sm">
                Every calculation includes detailed steps, formulas, and interpretations to help you learn.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-rose mb-2">⚡ Fast & Accurate</h3>
              <p className="text-subtle text-sm">
                Powered by Python's SciPy and NumPy libraries for reliable, precise calculations.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-iris mb-2">🎛️ Customizable</h3>
              <p className="text-subtle text-sm">
                Control decimal precision, confidence levels, and get results formatted exactly how you need.
              </p>
            </div>
          </div>
        </div>

        {/* Usage Tips */}
        <div className="mt-8 bg-surface rounded-lg p-6 border border-muted">
          <h3 className="text-lg font-semibold text-text mb-3">💡 Quick Tips</h3>
          <ul className="space-y-2 text-sm text-subtle">
            <li>• Use the decimal places control to match your assignment requirements</li>
            <li>• All results include both exact and rounded values for easy copying</li>
            <li>• Step-by-step solutions can be used to check your manual work</li>
            <li>• Save time on homework and focus on understanding the concepts</li>
          </ul>
        </div>
      </div>
    </div>
  )
}