"use client"

import { Hand, ArrowLeft, Play } from "lucide-react"
import Link from "next/link"
import { useState, useRef } from "react"

const SIGN_WORDS = [
  { word: "Help", video: "/images/help.mp4" },
  { word: "Yes", video: "/images/yes.mp4" },
  { word: "No", video: "/images/no.mp4" },
  { word: "Sorry", video: "/images/sorry.mp4" },
  { word: "How", video: "/images/how.mp4" },
  { word: "Bye", video: "/images/bye.mp4" },
  { word: "Where", video: "/images/where.mp4" },
  { word: "What", video: "/images/what.mp4" },
  { word: "Who", video: "/images/who.mp4" },
  { word: "Hello", video: "/images/hello.mp4" },
  { word: "Please", video: "/images/please.mp4" },
  { word: "Thanks", video: "/images/thanks.mp4" },
]

function VideoCard({ word, video }: { word: string; video: string | null }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)

  const handlePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
        videoRef.current.currentTime = 0
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const handleEnded = () => {
    setIsPlaying(false)
  }

  return (
    <div className="bg-card border-2 border-border rounded-2xl overflow-hidden">
      <div className="relative aspect-video bg-secondary cursor-pointer group" onClick={handlePlay}>
        {video ? (
          <>
            <video
              ref={videoRef}
              src={video}
              className="w-full h-full object-cover"
              onEnded={handleEnded}
              playsInline
            />
            {!isPlaying && (
              <div className="absolute inset-0 flex items-center justify-center bg-black/30 group-hover:bg-black/40 transition-colors">
                <div className="w-14 h-14 bg-primary rounded-full flex items-center justify-center shadow-lg">
                  <Play className="w-7 h-7 text-primary-foreground fill-primary-foreground ml-1" />
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-muted-foreground font-semibold">Coming Soon</p>
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="text-xl font-bold text-foreground text-center">{word}</h3>
      </div>
    </div>
  )
}

export default function GuidebookPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background border-b border-border">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-bold">Back</span>
          </Link>
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
              <Hand className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="text-2xl font-extrabold text-foreground">Handly</span>
          </div>
          <div className="w-20" /> {/* Spacer for centering */}
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-foreground mb-4">Signing Guidebook</h1>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto">
            Your library of basic signs. Click any card to watch the demonstration.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {SIGN_WORDS.map((item) => (
            <VideoCard key={item.word} word={item.word} video={item.video} />
          ))}
        </div>
      </main>
    </div>
  )
}
