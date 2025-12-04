"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import { useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Camera, CheckCircle, XCircle, Heart, HeartCrack, Flame } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { getUserData, completeLesson, type UserData } from "@/lib/user-store"

// Sound effects
const playSound = (sound: 'success' | 'fail' | 'streak') => {
  const audio = new Audio(`/sounds/${sound}.mp3`)
  audio.volume = 0.5
  audio.play().catch(() => {}) // Ignore autoplay errors
}

type Step = "video" | "practice"
type CompletionStep = "success" | "stats"

const LESSON_WORDS: Record<number, string[]> = {
  1: ["Help", "Yes", "No"],
  2: ["Help", "Yes", "No"],
}

const WORD_VIDEOS: Record<string, string> = {
  Help: "/images/help.mp4",
  Yes: "/images/yes.mp4",
  No: "/images/no.mp4",
}

const WORD_ACCURACY: Record<string, number> = {
  Help: 82,
  Yes: 79,
  No: 90,
}

const XP_PER_LESSON = 30

function getRandomAccuracy() {
  return Math.floor(Math.random() * 21) + 80
}

export default function LessonPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const lessonId = Number(searchParams.get("id")) || 1
  const WORDS = LESSON_WORDS[lessonId] || LESSON_WORDS[1]

  const [step, setStep] = useState<Step>("video")
  const [wordQueue, setWordQueue] = useState<string[]>([...WORDS])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [isComplete, setIsComplete] = useState(false)
  const [isGameOver, setIsGameOver] = useState(false)
  const [hearts, setHearts] = useState(3)
  const [breakingHeart, setBreakingHeart] = useState<number | null>(null)
  const [completionStep, setCompletionStep] = useState<CompletionStep>("success")
  const [userData, setUserData] = useState<UserData | null>(null)
  const [helpAttempts, setHelpAttempts] = useState(0)

  useEffect(() => {
    setUserData(getUserData())
  }, [])

  const currentWord = wordQueue[currentIndex]
  const totalRequired = WORDS.length
  const progressPercent = (correctCount / totalRequired) * 100

  const handleNext = () => {
    setStep("practice")
  }

  const handleLessonComplete = () => {
    const updated = completeLesson(lessonId, XP_PER_LESSON)
    setUserData(updated)
    setCompletionStep("stats")
  }

  const handleResult = (passed: boolean) => {
    if (passed) {
      setCorrectCount((c) => c + 1)
    } else {
      setBreakingHeart(hearts)
      const newHearts = hearts - 1

      setTimeout(() => {
        setHearts(newHearts)
        setBreakingHeart(null)

        if (newHearts <= 0) {
          setIsGameOver(true)
          return
        }
        setWordQueue((q) => [...q, currentWord])

        const newCorrectCount = correctCount
        if (newCorrectCount >= totalRequired) {
          setIsComplete(true)
        } else {
          setCurrentIndex((i) => i + 1)
          setStep("video")
        }
      }, 600)
      return
    }

    const newCorrectCount = passed ? correctCount + 1 : correctCount
    if (newCorrectCount >= totalRequired) {
      setIsComplete(true)
    } else {
      setCurrentIndex((i) => i + 1)
      setStep("video")
    }
  }

  // Play fail sound when game over
  useEffect(() => {
    if (isGameOver) {
      playSound('fail')
    }
  }, [isGameOver])

  if (isGameOver) {
    return (
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-24 text-center">
          <div className="w-24 h-24 bg-destructive rounded-full flex items-center justify-center mx-auto mb-6">
            <HeartCrack className="w-14 h-14 text-white" />
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold text-foreground mb-4">Out of Hearts!</h1>
          <p className="text-muted-foreground mb-8">Don't worry, practice makes perfect. Try again!</p>
          <Link href="/">
            <Button
              size="lg"
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg px-12 py-6 rounded-xl shadow-[0_4px_0_0] shadow-primary/50 hover:shadow-[0_2px_0_0] hover:translate-y-[2px] transition-all"
            >
              Back to Home
            </Button>
          </Link>
        </div>
      </main>
    )
  }

  // Play success sound when lesson completes
  useEffect(() => {
    if (isComplete && completionStep === "success") {
      playSound('success')
    }
  }, [isComplete, completionStep])

  // Play streak sound when showing stats
  useEffect(() => {
    if (isComplete && completionStep === "stats") {
      playSound('streak')
    }
  }, [isComplete, completionStep])

  if (isComplete) {
    if (completionStep === "success") {
      return (
        <main className="min-h-screen bg-background">
          <div className="container mx-auto px-4 py-24 text-center">
            <div className="w-24 h-24 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6 animate-[bounce_0.5s_ease-out]">
              <CheckCircle className="w-14 h-14 text-white" />
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-foreground mb-4">Lesson Complete!</h1>
            <p className="text-muted-foreground mb-8">You learned {WORDS.length} new signs</p>
            <Button
              size="lg"
              onClick={handleLessonComplete}
              className="bg-green-500 hover:bg-green-600 text-white font-bold text-lg px-12 py-6 rounded-xl shadow-[0_4px_0_0] shadow-green-700 hover:shadow-[0_2px_0_0] hover:translate-y-[2px] transition-all"
            >
              Continue
            </Button>
          </div>
        </main>
      )
    }

    const displayStreak = userData?.streak ?? 5
    const displayXp = userData?.xp ?? 1250
    const displayLevel = userData?.level ?? 5
    const displayLevelProgress = userData?.levelProgress ?? 65

    return (
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 text-center">
          <div className="relative w-32 h-32 mx-auto mb-6">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-28 h-28 bg-orange-500/20 rounded-full animate-[pulse_1.5s_ease-in-out_infinite]" />
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-24 h-24 bg-orange-500 rounded-full flex items-center justify-center animate-flame">
                <Flame className="w-14 h-14 text-white animate-flame-icon" />
              </div>
            </div>
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold text-orange-500 mb-2">{displayStreak} Day Streak!</h1>
          <p className="text-muted-foreground mb-10">You're on fire! Keep it going tomorrow.</p>

          <div className="bg-card border-2 border-border rounded-2xl p-6 max-w-sm mx-auto mb-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-muted-foreground font-semibold">XP Earned</span>
              <span className="text-2xl font-extrabold text-accent">+{XP_PER_LESSON} XP</span>
            </div>

            <div className="mb-2">
              <div className="flex items-center justify-between mb-2">
                <span className="text-foreground font-bold">Level {displayLevel}</span>
                <span className="text-muted-foreground text-sm">{displayLevelProgress}%</span>
              </div>
              <div className="h-4 bg-secondary rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${displayLevelProgress}%` }}
                />
              </div>
            </div>
          </div>

          <p className="text-muted-foreground mb-10">
            Total XP: <span className="text-foreground font-bold">{displayXp}</span>
          </p>

          <Button
            size="lg"
            onClick={() => router.push("/")}
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg px-12 py-6 rounded-xl shadow-[0_4px_0_0] shadow-primary/50 hover:shadow-[0_2px_0_0] hover:translate-y-[2px] transition-all"
          >
            Continue
          </Button>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between gap-4">
          <Link
            href="/"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors shrink-0"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-semibold">Exit</span>
          </Link>

          <div className="flex-1 max-w-md">
            <div className="h-3 bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          <div className="flex items-center gap-1 shrink-0">
            {[1, 2, 3].map((i) => (
              <div key={i} className="relative">
                {breakingHeart === i ? (
                  <div className="relative w-7 h-7">
                    <div
                      className="absolute inset-0 overflow-hidden animate-[crack-left_0.5s_ease-out_forwards]"
                      style={{ clipPath: "polygon(0 0, 50% 0, 50% 100%, 0 100%)" }}
                    >
                      <Heart className="w-7 h-7 text-red-500 fill-red-500" />
                    </div>
                    <div
                      className="absolute inset-0 overflow-hidden animate-[crack-right_0.5s_ease-out_forwards]"
                      style={{ clipPath: "polygon(50% 0, 100% 0, 100% 100%, 50% 100%)" }}
                    >
                      <Heart className="w-7 h-7 text-red-500 fill-red-500" />
                    </div>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="absolute w-1.5 h-1.5 bg-red-500 rounded-full animate-[particle-1_0.5s_ease-out_forwards]" />
                      <span className="absolute w-1 h-1 bg-red-500 rounded-full animate-[particle-2_0.5s_ease-out_forwards]" />
                      <span className="absolute w-1.5 h-1.5 bg-red-500 rounded-full animate-[particle-3_0.5s_ease-out_forwards]" />
                      <span className="absolute w-1 h-1 bg-red-500 rounded-full animate-[particle-4_0.5s_ease-out_forwards]" />
                    </div>
                  </div>
                ) : (
                  <Heart
                    className={`w-7 h-7 transition-all ${
                      i <= hearts ? "text-red-500 fill-red-500" : "text-muted-foreground/30"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12">
        {step === "video" ? (
          <VideoStep word={currentWord} onNext={handleNext} />
        ) : (
          <PracticeStep
            word={currentWord}
            onResult={handleResult}
            helpAttempts={helpAttempts}
            onHelpAttempt={() => setHelpAttempts((h) => h + 1)}
          />
        )}
      </div>
    </main>
  )
}

function VideoStep({ word, onNext }: { word: string; onNext: () => void }) {
  const videoUrl = WORD_VIDEOS[word]

  return (
    <div className="max-w-2xl mx-auto text-center">
      <h1 className="text-2xl md:text-3xl font-extrabold text-foreground mb-2">Learn the sign for "{word}"</h1>
      <p className="text-muted-foreground mb-8">Watch the video, then try it yourself</p>

      <div className="aspect-video bg-card rounded-2xl border-2 border-border mb-8 overflow-hidden">
        {videoUrl ? (
          <video src={videoUrl} controls autoPlay loop className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-secondary/50">
            <p className="text-muted-foreground font-semibold">Video not available</p>
          </div>
        )}
      </div>

      <Button
        size="lg"
        onClick={onNext}
        className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg px-12 py-6 rounded-xl shadow-[0_4px_0_0] shadow-primary/50 hover:shadow-[0_2px_0_0] hover:translate-y-[2px] transition-all"
      >
        Next
      </Button>
    </div>
  )
}

function PracticeStep({
  word,
  onResult,
  helpAttempts,
  onHelpAttempt,
}: {
  word: string
  onResult: (passed: boolean) => void
  helpAttempts: number
  onHelpAttempt: () => void
}) {
  const [status, setStatus] = useState<"idle" | "recording" | "analyzing" | "correct" | "incorrect">("idle")
  const [accuracy, setAccuracy] = useState<number>(0)
  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop())
      }
    }
  }, [])

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }
    } catch (err) {
      console.error("Failed to access webcam:", err)
    }
  }

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
  }

  const handleStartRecording = async () => {
    await startWebcam()
    setStatus("recording")
  }

  const handleStopRecording = () => {
    stopWebcam()
    setStatus("analyzing")

    setTimeout(() => {
      let willPass: boolean

      if (word === "Help") {
        if (helpAttempts === 0) {
          willPass = false
          onHelpAttempt()
        } else {
          willPass = true
        }
      } else {
        willPass = true
      }

      if (willPass) {
        setAccuracy(getRandomAccuracy())
        setStatus("correct")
        playSound('success')
      } else {
        setAccuracy(Math.floor(Math.random() * 30) + 20)
        setStatus("incorrect")
        playSound('fail')
      }
    }, 4000)
  }

  const handleContinue = () => {
    onResult(status === "correct")
  }

  return (
    <div className="max-w-2xl mx-auto text-center relative">
      <h1 className="text-2xl md:text-3xl font-extrabold text-foreground mb-2">Your turn! Sign "{word}"</h1>
      <p className="text-muted-foreground mb-8">Position yourself in the frame and sign</p>

      <div className="aspect-video bg-card rounded-2xl border-2 border-border mb-8 flex items-center justify-center relative overflow-hidden">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={`absolute inset-0 w-full h-full object-cover ${status === "recording" ? "block" : "hidden"}`}
        />

        {(status === "idle" || status === "analyzing" || status === "correct" || status === "incorrect") && (
          <>
            <div className="absolute inset-0 bg-secondary/50" />
            <div className="relative z-10 flex flex-col items-center gap-4">
              {status === "analyzing" ? (
                <>
                  <div className="w-20 h-20 rounded-full border-4 border-primary border-t-transparent animate-spin" />
                  <p className="text-foreground font-bold text-xl">Analyzing...</p>
                </>
              ) : (
                <>
                  <div className="w-20 h-20 bg-secondary rounded-full flex items-center justify-center border-4 border-border">
                    <Camera className="w-10 h-10 text-muted-foreground" />
                  </div>
                  <p className="text-muted-foreground font-semibold">
                    {status === "idle" ? "Camera Ready" : "Recording saved"}
                  </p>
                </>
              )}
            </div>
          </>
        )}

        {status === "recording" && (
          <div className="absolute top-4 left-4 flex items-center gap-2 z-10 bg-black/50 px-3 py-1.5 rounded-full">
            <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
            <span className="text-white font-bold text-sm">REC</span>
          </div>
        )}
      </div>

      {status === "idle" && (
        <Button
          size="lg"
          onClick={handleStartRecording}
          className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg px-12 py-6 rounded-xl shadow-[0_4px_0_0] shadow-primary/50 hover:shadow-[0_2px_0_0] hover:translate-y-[2px] transition-all"
        >
          Start Recording
        </Button>
      )}

      {status === "recording" && (
        <Button
          size="lg"
          onClick={handleStopRecording}
          className="bg-destructive hover:bg-destructive/90 text-white font-bold text-lg px-12 py-6 rounded-xl shadow-[0_4px_0_0] shadow-destructive/50 hover:shadow-[0_2px_0_0] hover:translate-y-[2px] transition-all"
        >
          Stop Recording
        </Button>
      )}

      {(status === "correct" || status === "incorrect") && (
        <div
          className={`fixed bottom-0 left-0 right-0 p-4 ${status === "correct" ? "bg-green-500" : "bg-destructive"}`}
        >
          <div className="container mx-auto flex items-center justify-between max-w-2xl">
            <div className="flex items-center gap-3">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  status === "correct" ? "bg-white/20" : "bg-white/20"
                }`}
              >
                {status === "correct" ? (
                  <CheckCircle className="w-6 h-6 text-white" />
                ) : (
                  <XCircle className="w-6 h-6 text-white" />
                )}
              </div>
              <div className="text-left">
                <p className="text-white font-bold text-lg">
                  {status === "correct" ? "Great job!" : "Not quite - try again later!"}
                </p>
                <p className="text-white/80 font-semibold">Accuracy: {accuracy}%</p>
              </div>
            </div>
            <Button
              size="lg"
              onClick={handleContinue}
              className="bg-white hover:bg-white/90 text-green-600 font-bold px-8 py-3 rounded-xl"
              style={{ color: status === "correct" ? "#16a34a" : "#dc2626" }}
            >
              Continue
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
