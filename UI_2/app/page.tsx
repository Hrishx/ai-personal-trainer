'use client'

import { useState } from 'react'
import WorkoutSelection from '@/components/screens/WorkoutSelection'
import ExerciseDemo from '@/components/screens/ExerciseDemo'
import LiveCoaching from '@/components/screens/LiveCoaching'
import WorkoutSummary from '@/components/screens/WorkoutSummary'

type Screen = 'selection' | 'demo' | 'coaching' | 'summary'

export default function Home() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('selection')
  const [selectedExercise, setSelectedExercise] = useState<string | null>(null)

  const handleSelectExercise = (exercise: string) => {
    setSelectedExercise(exercise)
    setCurrentScreen('demo')
  }

  const handleStartCoaching = () => {
    setCurrentScreen('coaching')
  }

  const handleFinishWorkout = () => {
    setCurrentScreen('summary')
  }

  const handleRestartWorkout = () => {
    setCurrentScreen('selection')
    setSelectedExercise(null)
  }
  const handleBackToSelection = () => {
  setCurrentScreen('selection')
  }
  

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-green-50 via-white to-teal-50 flex items-center justify-center px-4 py-10">

      {/* Main Container */}
      <div className="w-full max-w-6xl">

        {currentScreen === 'selection' && (
          <WorkoutSelection onSelectExercise={handleSelectExercise} />
        )}

        {currentScreen === 'demo' && selectedExercise && (
          <div className="animate-fadeIn">
            <ExerciseDemo
              exercise={selectedExercise}
              onStartCoaching={handleStartCoaching}
              onBack={handleBackToSelection}
            />
          </div>
        )}

        {currentScreen === 'coaching' && selectedExercise && (
          <div className="animate-fadeIn">
            <LiveCoaching
              exercise={selectedExercise}
              onFinishWorkout={handleFinishWorkout}
            />
          </div>
        )}

        {currentScreen === 'summary' && selectedExercise && (
          <div className="animate-fadeIn">
            <WorkoutSummary
              exercise={selectedExercise}
              onRestart={handleRestartWorkout}
            />
          </div>
        )}

      </div>
    </div>
  )
}