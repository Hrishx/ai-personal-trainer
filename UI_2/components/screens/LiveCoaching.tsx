// LiveCoaching.tsx

"use client"

import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { CheckCircle2 } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'

interface LiveCoachingProps {
  exercise: string
  onFinishWorkout: (data: any) => void
}


// 🔥 MODE SWITCH
const MODE: "video" | "camera" = "camera"


export default function LiveCoaching({ exercise, onFinishWorkout }: LiveCoachingProps) {

  const isSending = useRef(false)
  const [isFinished, setIsFinished] = useState(false)
  const [data, setData] = useState<any>(null)
  const [workoutTime, setWorkoutTime] = useState(0)
  const [loading, setLoading] = useState(false)
  const [showSummaryLoader, setShowSummaryLoader] = useState(false)

  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)
  const sessionIdRef = useRef(Date.now())

  const detectionBuffer = useRef<string[]>([])
  const [stableDetectedExercise, setStableDetectedExercise] = useState<string | null>(null)

  // ⏱ TIMER
  useEffect(() => {
    if (isFinished) return

    const timer = setInterval(() => {
      setWorkoutTime(prev => prev + 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [isFinished, exercise])

  useEffect(() => {
    const reset = async () => {
      console.log("🧹 NEW WORKOUT RESET")

      // 🔥 NEW SESSION ID
      sessionIdRef.current = Date.now()

      // 🔥 STOP OLD INTERVAL
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }

      // 🔥 RESET BACKEND
      await fetch("http://127.0.0.1:8000/reset_session", {
        method: "POST"
      })

      localStorage.clear()

      // 🔥 HARD RESET UI
      setData({
        reps: 0,
        score: 0,
        fatigue: 0,
        feedback: "Analyzing..."
      })

      setWorkoutTime(0)
      setIsFinished(false)
      setShowSummaryLoader(false)
    }

    reset()
  }, [exercise]) // 🔥 THIS IS THE FIX

const smoothZoom = useRef(1)
const [, forceUpdate] = useState(0)
// ✅ CORRECT PLACE (OUTSIDE other useEffect)
useEffect(() => {
  if (data?.zoom) {
    smoothZoom.current =
      smoothZoom.current * 0.8 + data.zoom * 0.2
    forceUpdate(prev => prev + 1) // 🔥 trigger re-render
  }
}, [data?.zoom])

  // 🎥 VIDEO / CAMERA SETUP
  useEffect(() => {
    let isMounted = true

    async function startInput() {
      try {
        if (MODE === "camera") {
          const stream = await navigator.mediaDevices.getUserMedia({ video: true })

          if (!isMounted) return
          streamRef.current = stream

          if (videoRef.current) {
            videoRef.current.srcObject = stream
          }

        } else {
          if (videoRef.current) {
            videoRef.current.srcObject = null

            videoRef.current.src = "/video/squats.mp4" // ✅ FIXED PATH
            videoRef.current.loop = true
            videoRef.current.muted = true
            videoRef.current.playsInline = true

            videoRef.current.onloadeddata = () => {
              videoRef.current?.play()
            }
          }
        }

      } catch (err) {
        console.error("Camera error:", err)
      }
    }

    startInput()

    return () => {
      stopInput()
      isMounted = false
    }
  }, [])

  // 🔥 FRAME SENDING PIPELINE
  useEffect(() => {
  if (isFinished) return

  let interval: NodeJS.Timeout
  

  const sendFrame = async () => {
    const currentSession = sessionIdRef.current

    if (isFinished) {
      isSending.current = false
      return
    }

    if (!videoRef.current) return
    if (isSending.current) return

    const video = videoRef.current
    if (video.readyState < 3 || video.videoWidth === 0) return

    if (isSending.current) return
    isSending.current = true

    if (!canvasRef.current) {
      canvasRef.current = document.createElement("canvas")
    }

    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    if (!ctx) {
      isSending.current = false
      return
    }

    ctx.drawImage(video, 0, 0)

    canvas.toBlob(async (blob) => {
      if (!blob) return

      try {
        const res = await fetch("http://127.0.0.1:8000/process_frame", {
          method: "POST",
          body: blob
        })

        if (!res.ok) return

        const result = await res.json()

        // 🔥 IGNORE OLD RESPONSES
        if (currentSession !== sessionIdRef.current) return

        // =========================
        // 🔥 SMART EXERCISE STABILIZER
        // =========================

        const detected = result?.detected_exercise

        if (detected && detected !== "None") {
          detectionBuffer.current.push(detected)

          // keep last 10 frames
          if (detectionBuffer.current.length > 10) {
            detectionBuffer.current.shift()
          }

          // count frequency
          const counts: Record<string, number> = {}

          detectionBuffer.current.forEach((ex) => {
            counts[ex] = (counts[ex] || 0) + 1
          })

          // get dominant exercise
          const dominant = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]

          // only accept if stable
          if (dominant && dominant[1] >= 6) {
            setStableDetectedExercise(dominant[0])
          }
        }

        // =========================
        // 🔥 FINAL STATE UPDATE
        // =========================

        setData({
          reps: result?.reps ?? 0,
          score: result?.score ?? 0,
          fatigue: result?.fatigue ?? 0,
          feedback: result?.feedback ?? "Analyzing...",
          detected_exercise: result?.detected_exercise // 🔥 IMPORTANT
        })

      } catch (err) {
        console.warn("⚠️ Frame skipped")
      }

      isSending.current = false

    }, "image/jpeg", 0.7)
  }

  const timeout = setTimeout(() => {
    intervalRef.current = setInterval(sendFrame, 500)
  }, 1000)

  return () => {
    clearTimeout(timeout)
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }
}, [isFinished , exercise])

  // 🛑 STOP INPUT
  const stopInput = () => {
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
        streamRef.current = null
      }

      if (videoRef.current) {
        videoRef.current.pause()
        videoRef.current.srcObject = null
      }

    } catch (err) {
      console.error("Stop error:", err)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const reps = data?.reps ?? 0
  const score = data?.score ?? 80
  const feedback = data?.feedback ?? "Analyzing..."

  const selectedExercise = exercise
  const detectedExercise = stableDetectedExercise

  const isMismatch =
    detectedExercise &&
    detectedExercise !== "None" &&
    selectedExercise.toLowerCase() !== detectedExercise.toLowerCase()

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-50 to-gray-100 px-4 py-8 text-gray-900">
      <div className="mx-auto max-w-7xl">

        {/* VIDEO */}
        <div className="mb-8 rounded-3xl overflow-hidden bg-black shadow-xl border border-gray-200">
          <div className="relative aspect-video w-full">

            {isFinished ? (
              <div className="absolute inset-0 bg-black flex items-center justify-center">
                <div className="text-center text-white">
                  <p className="text-xl font-semibold animate-pulse">
                    Generating AI Report...
                  </p>
                  <p className="text-sm text-gray-400 mt-2">
                    Please wait a few seconds
                  </p>
                </div>
              </div>
            ) : (
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="absolute inset-0 w-full h-full object-contain border-4 border-red-500 transition-transform duration-300"
                style={{
                  transform: `scale(${smoothZoom.current})`
                }}
              />
            )}

            {/* 🔥 ADD THIS HERE */}
            {isMismatch && (
              <div className="absolute top-2 left-1/2 -translate-x-1/2 bg-red-500 text-white px-4 py-2 rounded-lg text-sm z-50">
                ⚠️ You're doing {detectedExercise} but selected {selectedExercise}
              </div>
            )}

            <div className="absolute inset-0 bg-black/20" />

            {!isFinished && !showSummaryLoader && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <p className="text-green-400 text-lg font-semibold">
                  AI analyzing posture...
                </p>
              </div>
            )}
            {/* 🔥 LIVE FEEDBACK OVERLAY */}
            {!isFinished && feedback !== "Analyzing..." && (
              <div className="absolute bottom-20 left-1/2 -translate-x-1/2 bg-black/70 text-white px-4 py-2 rounded-lg text-sm">
                {feedback}
              </div>
            )}

            {/* TOP LEFT */}
            <div className="absolute top-4 left-4 bg-white/80 backdrop-blur-md border border-gray-200 p-3 rounded-xl shadow">
              <p className="text-xs text-gray-500">EXERCISE</p>
              <p className="font-semibold text-green-600">{exercise}</p>
              <p className="text-sm">Reps: {reps}</p>
            </div>

            {/* TOP RIGHT */}
            <div className="absolute top-4 right-4 bg-white/80 backdrop-blur-md border border-gray-200 p-3 rounded-xl text-center shadow">
              <CheckCircle2 className="text-green-500 mx-auto animate-pulse" />
              <p className="text-xs text-gray-500">AI Active</p>
            </div>

            {/* FORM SCORE */}
            <div className="absolute bottom-4 left-4 right-4 bg-white/80 backdrop-blur-md border border-gray-200 p-3 rounded-xl shadow">
              <p className="text-sm mb-1 text-gray-600">Form Score</p>
              <div className="w-full h-2 bg-gray-200 rounded-full">
                <div
                  className="h-2 bg-gradient-to-r from-green-400 to-teal-400 rounded-full transition-all"
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>

          </div>
        </div>

        {/* METRICS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {[
            { label: "Reps", value: reps },
            { label: "Score", value: `${score}%` },
            { label: "Fatigue", value: `${data?.fatigue || 0}%` },
            { label: "Time", value: formatTime(workoutTime) },
          ].map((item, i) => (
            <Card key={i} className="p-4 bg-white border border-gray-200 rounded-xl shadow-sm">
              <p className="text-xs text-gray-500">{item.label}</p>
              <p className="text-xl font-bold">{item.value}</p>
            </Card>
          ))}
        </div>

        {/* FEEDBACK */}
        <Card className="p-4 mb-4 bg-white border border-gray-200 shadow-sm">
          <p className="text-yellow-600 text-sm mb-2 font-medium">
            AI Feedback
          </p>
          <p className="text-sm text-gray-700">
            {feedback}
          </p>
        </Card>

        {/* FINISH */}
        {/* const [isFinished, setIsFinished] = useState(false) */}

        <Button
          disabled={isFinished || loading} // ✅ also add loading here
          onClick={async () => {
            if (isFinished) return

            setIsFinished(true)
            setLoading(true)
            setShowSummaryLoader(true)

            // 🔥 STOP FRAME LOOP
            if (intervalRef.current) {
              clearInterval(intervalRef.current)
              intervalRef.current = null
            }

            // 🔥 STOP VIDEO
            if (videoRef.current) {
              videoRef.current.pause()
              videoRef.current.srcObject = null
            }

            // try {
            //   await fetch("http://127.0.0.1:8000/reset_session", {
            //     method: "POST"
            //   })
            // } catch (e) {
            //   console.log("⚠️ reset after finish failed")
            // }

            // 🔥 STOP CAMERA
            stopInput()

            // 🔥 RESET FRONTEND STATE
            // setData(null)

            try {
              console.log("🔥 Generating summary...")

              const res = await fetch("http://127.0.0.1:8000/generate_summary", {
                method: "POST"
              })

              const data = await res.json()
              // ✅ RESET AFTER SUMMARY (CORRECT PLACE)
              await fetch("http://127.0.0.1:8000/reset_session", {
                method: "POST"
              })
              
              console.log("✅ LLM REPORT:", data)

              localStorage.setItem("totalReps", String(data?.total_reps || 0))
              localStorage.setItem("avgScore", String(data?.average_score || 0))
              localStorage.setItem("fatigue", String(data?.fatigue || 0))
              localStorage.setItem("duration", String(workoutTime)) // ✅ VERY IMPORTANT
              localStorage.setItem("ai_report", JSON.stringify(data))

              onFinishWorkout(data)

            } catch (err) {
              console.log("❌ ERROR:", err)
            } finally {
              setLoading(false) // 🔥 THIS WAS MISSING
            }
          }}
          className="w-full mt-2 bg-red-500 hover:bg-red-600 transition">
          {loading ? "Generating Report..." : "Finish Workout"} {/* 🔥 UI improvement */}
        </Button>
      </div>
    </div>
  )
}