'use client'

import { Dumbbell } from 'lucide-react'

interface WorkoutSelectionProps {
  onSelectExercise: (exercise: string) => void
}

const exercises = [
  {
    name: 'Push-up',     // ✅ internal
    label: 'Push-ups',   // ✅ UI
    image: 'push-up',
    difficulty: 'Beginner',
    muscleGroup: 'Chest & Triceps',
  },
  {
    name: 'Squat',
    label: 'Squats',
    image: 'squat',
    difficulty: 'Intermediate',
    muscleGroup: 'Legs & Glutes',
  },
  {
    name: 'Lunge',
    label: 'Lunges',
    image: 'lunge',
    difficulty: 'Intermediate',
    muscleGroup: 'Quads and Core',
  },
  {
    name: 'Plank',
    label: 'Plank',
    image: 'plank',
    difficulty: 'Beginner',
    muscleGroup: 'Full Body Core',
  },
]

export default function WorkoutSelection({ onSelectExercise }: WorkoutSelectionProps) {
  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-50 via-white to-gray-100 px-6 py-12">

      <div className="mx-auto max-w-6xl">

        {/* HEADER */}
        <div className="mb-16 text-center">
          <div className="mb-6 flex justify-center">
            <div className="rounded-full bg-gradient-to-r from-green-400 to-teal-400 p-4 shadow-xl">
              <Dumbbell className="h-8 w-8 text-white" />
            </div>
          </div>

          <h1 className="text-5xl font-extrabold text-gray-800">
            AI Fitness <span className="text-teal-500">Coach</span>
          </h1>

          <p className="mt-4 text-lg text-gray-500">
            Choose your workout and let AI guide your form
          </p>
        </div>

        {/* GRID */}
        <div className="grid gap-8 md:grid-cols-2">

          {exercises.map((exercise) => (
            <div
              key={exercise.name}
              onClick={() => onSelectExercise(exercise.name)} // ✅ IMPORTANT
              className="group relative p-6 rounded-3xl bg-white shadow-xl transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl cursor-pointer"
            >

              <div className="relative z-10">

                {/* IMAGE */}
                <div className="mb-6 flex items-center justify-center rounded-2xl h-48 overflow-hidden">
                  <img
                    src={`/images/${exercise.image}.jpeg`}
                    alt={exercise.label}
                    className="h-full w-full object-contain group-hover:scale-105 transition duration-300"
                  />
                </div>

                {/* TITLE */}
                <h3 className="text-xl font-bold text-gray-800 mb-2">
                  {exercise.label}
                </h3>

                {/* BADGE */}
                <span className={`inline-block px-3 py-1 text-xs rounded-full mb-3 font-medium ${
                  exercise.difficulty === 'Beginner'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-yellow-200 text-yellow-800'
                }`}>
                  {exercise.difficulty}
                </span>

                {/* TARGET */}
                <p className="text-gray-500 text-sm mb-4">
                  Target: <span className="text-gray-700 font-semibold">{exercise.muscleGroup}</span>
                </p>

                {/* BUTTON */}
                <button className="w-full py-3 rounded-full text-white font-semibold bg-gradient-to-r from-green-400 to-teal-400 shadow-lg hover:scale-[1.02] transition">
                  Start →
                </button>

              </div>
            </div>
          ))}

        </div>

      </div>
    </div>
  )
}