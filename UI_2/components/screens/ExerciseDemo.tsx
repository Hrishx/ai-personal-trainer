"use client"

import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { ChevronLeft } from 'lucide-react'
import { useState } from 'react'

interface ExerciseDemoProps {
  exercise: string
  onStartCoaching: () => void
  onBack: () => void
}

const exerciseInstructions: Record<string, string[]> = {
  Squat: [
    'Keep chest upright and shoulders back',
    'Knees aligned with toes',
    'Lower hips below knee level',
    'Push through heels to return to start',
  ],
  'Push-up': [
    'Hands shoulder-width apart',
    'Body in straight line from head to heels',
    'Lower chest toward floor',
    'Push back to starting position',
  ],
  Lunge: [
    'Step forward with one leg',
    'Lower hips until both knees at 90 degrees',
    'Keep front knee aligned over ankle',
    'Push back to starting position',
  ],
  Plank: [
    'Hands under shoulders, body in straight line',
    'Core engaged, no sagging hips',
    'Keep neck neutral',
    'Hold position for desired duration',
  ],
}

const exerciseFrames: Record<string, string[]> = {
  'Push-up': [
    '/images/push_up_frames/p1.jpeg',
    '/images/push_up_frames/p2.jpeg',
    '/images/push_up_frames/p3.jpeg',
    '/images/push_up_frames/p4.jpg',
  ],
  Squat: [
    '/images/squat_frames/s1.jpeg',
    '/images/squat_frames/s2.jpeg',
    '/images/squat_frames/s3.jpeg',
    '/images/squat_frames/s4.jpeg',
  ],
  Lunge: [
    '/images/lunges_frames/l1.jpeg',
    '/images/lunges_frames/l2.jpeg',
    '/images/lunges_frames/l3.jpeg',
    '/images/lunges_frames/l4.jpeg',
  ],
  Plank: [
    '/images/plank_frames/pl1.jpeg',
    '/images/plank_frames/pl2.jpeg',
    '/images/plank_frames/pl3.jpeg',
    '/images/plank_frames/pl4.jpeg',
  ],
}

export default function ExerciseDemo({
  exercise,
  onStartCoaching,
  onBack,
}: ExerciseDemoProps) {

  const [animationFrame, setAnimationFrame] = useState(0)

  const frames = exerciseFrames[exercise] || []

  const animateFrame = () => {
    if (frames.length === 0) return
    setAnimationFrame((prev) => (prev + 1) % frames.length)
  }

  return (
    <div className="min-h-screen w-full bg-gray-50 px-4 py-8">
      <div className="mx-auto max-w-4xl">

        {/* HEADER */}
        <div className="mb-8 flex items-center gap-4">
          <button
            onClick={onBack}
            aria-label="Go back"
            className="rounded-full border border-gray-200 bg-white p-2 hover:bg-gray-100 transition"
          >
            <ChevronLeft className="h-6 w-6 text-gray-700" />
          </button>

          <h1 className="text-3xl font-bold text-gray-800">
            Learn the Movement
          </h1>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">

          {/* 🔥 PREMIUM DEMO CARD */}
          <Card className="group relative flex h-100 items-center justify-center rounded-2xl border border-gray-200 bg-gradient-to-br from-gray-50 to-gray-100 shadow-md transition-all duration-500 hover:-translate-y-2 hover:shadow-xl overflow-hidden">

            {/* ✨ GLOW */}
            <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition duration-500 bg-gradient-to-r from-white-200 via-transparent to-white-200 blur-xl"></div>

              <div className="relative h-full w-full flex flex-col">

                {/* IMAGE AREA (LOCKED CENTER) */}
                <div className="flex-1 flex items-center justify-center">
                  {frames.length > 0 && (
                    <img
                      src={frames[animationFrame]}
                      alt="movement"
                      className="h-64 object-contain transition duration-300 group-hover:scale-105"
                    />
                  )}
                </div>

                {/* BOTTOM FIXED AREA */}
                <div className="flex flex-col items-center pt-2 pb-6">

                {/* Movement Demo */}
                <p className="text-xs text-gray-500 tracking-wide leading-none mb-1">
                  Movement Demo
                </p>

                {/* Frame */}
                <p className="text-lg font-semibold text-gray-600 leading-tight">
                  Frame {animationFrame + 1} of {frames.length}
                </p>

                {/* BUTTON */}
                <button
                  onClick={animateFrame}
                  className="mt-2 px-5 py-2 rounded-full bg-gray-500 text-center text-sm font-semibold hover:bg-black text-white transition"
                >
                  Next Frame
                </button>

              </div>
            </div>
          </Card>

          {/* RIGHT SIDE */}
          <div className="flex flex-col gap-6">

            <h2 className="text-2xl font-semibold text-gray-900">
              {exercise}
            </h2>

            {/* INSTRUCTIONS */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Step-by-Step Instructions:
              </h3>

              <div className="space-y-4">
                {exerciseInstructions[exercise]?.map((step, i) => (
                  <div key={i} className="flex items-start gap-4">

                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-300 text-black-700 font-semibold text-sm">
                      {i + 1}
                    </div>

                    <p className="text-gray-700 text-sm leading-relaxed">
                      {step}
                    </p>

                  </div>
                ))}
              </div>
            </div>

            {/* TIPS */}
            <div className="rounded-xl border border-gray-200 bg-gray-100 p-4">
              <p className="text-sm font-semibold text-blue-500 mb-2">
                💡 Key Tips:
              </p>

              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Keep movements controlled and smooth</li>
                <li>• Maintain proper form over speed</li>
                <li>• Engage your core throughout</li>
              </ul>
            </div>

            {/* BUTTON */}
            <Button
              onClick={onStartCoaching}
              className="mt-2 w-full bg-gradient-to-r from-green-400 to-teal-400 text-white py-4 text-sm font-semibold hover:scale-[1.02] transition"
            >
              Start Live Coaching
            </Button>

          </div>
        </div>
      </div>
    </div>
  )
}