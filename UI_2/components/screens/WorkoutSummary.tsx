// Workout Summary

'use client'

import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Trophy, TrendingUp, AlertTriangle, Heart } from 'lucide-react'
import { useEffect, useState } from 'react'

interface WorkoutSummaryProps {
  exercise: string
  onRestart: () => void
}

export default function WorkoutSummary({ exercise, onRestart }: WorkoutSummaryProps) {

  // 🔥 NEW STATE
  const [stats, setStats] = useState<any>(null)
  // const [report, setReport] = useState<any>(null)

  // 🔥 FETCH FROM BACKEND
  useEffect(() => {
    const interval = setInterval(() => {
      const report = localStorage.getItem("ai_report")

      if (report) {
        setStats({
          totalReps: Number(localStorage.getItem("totalReps") || 0),
          avgFormScore: Number(localStorage.getItem("avgScore") || 0),
          fatigueLevel: Number(localStorage.getItem("fatigue") || 0),
          duration: Number(localStorage.getItem("duration") || 0),
          errors: [],
          report: JSON.parse(report)
        })

        clearInterval(interval) // ✅ stop checking once found
      }
    }, 500) // check every 0.5 sec

    return () => clearInterval(interval)
  }, [])

  // 🔥 SAFE FALLBACK
  const totalReps = stats?.totalReps ?? 0
  const avgFormScore = stats?.avgFormScore ?? 0
  const fatigueLevel = stats?.fatigueLevel ?? 0
  const detectedErrors = stats?.errors ?? ['No major issues']

  return (
    <div className="min-h-screen w-full bg-background px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-4xl">

        {/* Header */}
        <div className="mb-12 text-center">
          <div className="mb-6 flex items-center justify-center">
            <Trophy className="h-16 w-16 text-primary animate-bounce" />
          </div>
          <h1 className="text-5xl font-bold mb-3 text-foreground">Workout Complete!</h1>
          <p className="text-xl text-muted-foreground">
            Great job! Here's your AI coaching analysis for <span className="text-primary font-semibold">{exercise}</span>
          </p>
        </div>

        {/* Metrics */}
        <div className="grid gap-4 sm:grid-cols-4 mb-12">

          <Card className="bg-card border-border p-6 text-center soft-shadow">
            <p className="text-sm font-semibold text-muted-foreground uppercase mb-2">Total Reps</p>
            <p className="text-4xl font-bold text-primary mb-2">{totalReps}</p>
            <p className="text-xs text-muted-foreground">AI tracked</p>
          </Card>

          <Card className="bg-card border-border p-6 text-center soft-shadow">
            <p className="text-sm font-semibold text-muted-foreground uppercase mb-2">Form Score</p>
            <p className="text-4xl font-bold text-secondary mb-2">{avgFormScore}%</p>
            <p className="text-xs text-muted-foreground">AI evaluated</p>
          </Card>

          <Card className="bg-card border-border p-6 text-center soft-shadow">
            <p className="text-sm font-semibold text-muted-foreground uppercase mb-2">Fatigue</p>
            <p className="text-4xl font-bold text-primary mb-2">{fatigueLevel}%</p>
            <p className="text-xs text-muted-foreground">Estimated</p>
          </Card>

          <Card className="bg-card border-border p-6 text-center soft-shadow">
            <p className="text-sm font-semibold text-muted-foreground uppercase mb-2">Duration</p>
            <p className="text-4xl font-bold text-foreground mb-2">{stats?.duration ? `${stats.duration}s` : "--"}</p>
            <p className="text-xs text-muted-foreground">Session time</p>
          </Card>

        </div>

        {/* AI REPORT */}
        <div className="space-y-6">
          <h2 className="text-2xl m-3 font-bold mb-6 text-foreground">AI Coaching Report</h2>

          {/* Overview */}
          <Card className="bg-card border-border mb-5 p-6 soft-shadow-md">
            <div className=" flex items-center gap-2">
              <TrendingUp className="h-6 w-6 text-primary" />
              <h3 className="text-lg font-bold text-primary">Performance Overview</h3>
            </div>
            <p className="text-card-foreground mb-4 leading-relaxed">
              You completed {totalReps} reps with an average score of {avgFormScore}%.
              Your consistency and control are improving. Keep focusing on form.
            </p>
            {/* 🔥 LLM REPORT (ADD THIS HERE) */}
            <p className="text-card-foreground leading-relaxed text-[15px] leading-7 mt-4 bg-gray-50 p-4 rounded-xl border whitespace-pre-line">
              {!stats?.report
                ? "Generating AI report..."
                : stats.report.performance}
            </p>
          </Card>

          {/* Errors */}
          <Card className="bg-card border-border p-6 soft-shadow ">
            <div className="flex items-center gap-3">
              <AlertTriangle className="h-6 w-6 text-accent" />
              <h3 className="text-lg font-bold text-accent">Form Corrections Needed</h3>
            </div>
            {/* 🔥 LLM REPORT (ADD THIS HERE) */}
            <p className="text-card-foreground leading-relaxed text-[15px] leading-7 mt-4 bg-gray-50 p-4 rounded-xl border whitespace-pre-line">
              {!stats?.report
                  ? "Generating AI report..."
                  : stats.report.corrections}
            </p>

            {/* <div className="space-y-4">
              {detectedErrors.map((error: string, index: number) => (
                <div key={index} className="rounded-2xl bg-accent/10 border border-accent/20 p-4">
                  <p className="font-semibold text-accent mb-1">{error}</p>
                  <p className="text-sm text-card-foreground">
                    Improve this area to enhance performance and prevent injury.
                  </p>
                </div>
                
              ))}
            </div> */}
          </Card>

          {/* Injury */}
          <Card className="bg-card border-border p-6 soft-shadow">
            <div className="flex items-center gap-3">
              <Heart className="h-6 w-6 text-secondary" />
              <h3 className="text-lg font-bold text-secondary">Injury Prevention</h3>
            </div>
            {/* 🔥 LLM REPORT (ADD THIS HERE) */}
            <div className="text-card-foreground leading-relaxed text-[15px] mt-4 bg-gray-50 p-4 rounded-xl border whitespace-pre-line">
              {!stats?.report
                ? "Generating AI report..."
                : stats.report.injury || "No injury insights generated by AI."}
            </div>
            {/* <p className="text-card-foreground leading-relaxed mb-4">
              Maintain proper alignment and controlled movement to avoid injuries.
            </p> */}
          </Card>

          {/* Motivation */}
          <Card className="p-6 bg-gray-50 border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              ⭐ Great Work!
            </h3>
            {/* 🔥 LLM REPORT (ADD THIS HERE) */}
            <div className="text-card-foreground leading-relaxed text-[15px] mt-4 bg-gray-50 p-4 rounded-xl border whitespace-pre-line">
              {!stats?.report
                ? "Generating AI report..."
                : stats.report.motivation || "AI did not generate motivation insights."}
            </div>
            <p className="text-gray-600 mb-4">
              You're improving consistently. Keep pushing your limits!
            </p>
          </Card>
        </div>

        {/* Button */}
        <div className="mt-12 text-center">
          <Button
            onClick={async () => {
              await fetch("http://127.0.0.1:8000/reset_session", {
                method: "POST"
              })

              localStorage.clear()
              onRestart()
            }}
            className="bg-gradient-to-r from-green-400 to-teal-500 text-white px-6 py-3"
          >
            Start Another Workout
          </Button>
        </div>

      </div>
    </div>
  )
}