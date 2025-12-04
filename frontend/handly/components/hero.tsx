"use client"

import { Star, Lock, CheckCircle, Trophy } from "lucide-react"
import Link from "next/link"
import { useEffect, useState } from "react"
import { getUserData, type UserData } from "@/lib/user-store"

export function Hero() {
  const [user, setUser] = useState<UserData | null>(null)

  useEffect(() => {
    setUser(getUserData())
  }, [])

  const isLesson1Complete = user?.completedLessons.includes(1) ?? false
  const isLesson2Unlocked = isLesson1Complete
  const isLesson2Complete = user?.completedLessons.includes(2) ?? false

  return (
    <section className="py-16 md:py-24">
      <div className="container mx-auto px-4">
        {/* Top text section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-extrabold text-foreground leading-tight mb-6 text-balance">
            Learn Signing the <span className="text-primary">fun way</span>
          </h1>

          <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto text-pretty">
            Master Sign Language through bite-sized lessons. Earn XP, unlock achievements, and build your streak.
          </p>
        </div>

        {/* Skill Tree Roadmap - Center piece */}
        <div className="relative max-w-lg mx-auto">
          {/* Unit header */}
          <div className="bg-primary rounded-2xl p-4 mb-8 flex items-center justify-between">
            <div>
              <p className="text-primary-foreground/80 text-sm font-semibold">UNIT 1</p>
              <p className="text-primary-foreground font-bold text-lg">Basics</p>
            </div>
            <Link href="/guidebook">
              <div className="bg-primary-foreground/20 px-3 py-1 rounded-lg hover:bg-primary-foreground/30 transition-colors cursor-pointer">
                <span className="text-primary-foreground font-bold text-sm">GUIDEBOOK</span>
              </div>
            </Link>
          </div>

          {/* Skill tree nodes */}
          <div className="flex flex-col items-center gap-6">
            {/* Node 1 - Complete or Active */}
            <div className="relative">
              {isLesson1Complete ? (
                <button className="w-20 h-20 bg-primary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-primary/50 border-4 border-primary">
                  <CheckCircle className="w-10 h-10 text-primary-foreground" />
                </button>
              ) : (
                <Link href="/lesson?id=1">
                  <button className="w-20 h-20 bg-primary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-primary/50 hover:shadow-[0_3px_0_0] hover:translate-y-[3px] transition-all border-4 border-primary animate-pulse-glow">
                    <Star className="w-10 h-10 text-primary-foreground fill-primary-foreground" />
                  </button>
                </Link>
              )}
              {!isLesson1Complete && (
                <div className="absolute -top-2 -right-2 bg-accent text-accent-foreground text-xs font-bold px-2 py-1 rounded-lg">
                  START
                </div>
              )}
            </div>

            {/* Connector */}
            <div className="w-1 h-6 bg-border rounded-full" />

            {/* Node 2 - Unlocked after lesson 1 */}
            {isLesson2Unlocked ? (
              isLesson2Complete ? (
                <button className="w-20 h-20 bg-primary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-primary/50 border-4 border-primary">
                  <CheckCircle className="w-10 h-10 text-primary-foreground" />
                </button>
              ) : (
                <div className="relative">
                  <Link href="/lesson?id=2">
                    <button className="w-20 h-20 bg-primary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-primary/50 hover:shadow-[0_3px_0_0] hover:translate-y-[3px] transition-all border-4 border-primary">
                      <Star className="w-10 h-10 text-primary-foreground fill-primary-foreground" />
                    </button>
                  </Link>
                  <div className="absolute -top-2 -right-2 bg-accent text-accent-foreground text-xs font-bold px-2 py-1 rounded-lg">
                    NEW
                  </div>
                </div>
              )
            ) : (
              <button className="w-20 h-20 bg-secondary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-border border-4 border-border cursor-not-allowed">
                <CheckCircle className="w-10 h-10 text-muted-foreground" />
              </button>
            )}

            {/* Connector */}
            <div className="w-1 h-6 bg-border rounded-full" />

            {/* Node 3 - Locked */}
            <button className="w-20 h-20 bg-secondary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-border border-4 border-border cursor-not-allowed">
              <Star className="w-10 h-10 text-muted-foreground" />
            </button>

            {/* Connector */}
            <div className="w-1 h-6 bg-border rounded-full" />

            {/* Node 4 - Locked */}
            <button className="w-20 h-20 bg-secondary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-border border-4 border-border cursor-not-allowed">
              <Lock className="w-10 h-10 text-muted-foreground" />
            </button>

            {/* Connector */}
            <div className="w-1 h-6 bg-border rounded-full" />

            {/* Node 5 - Trophy (checkpoint) */}
            <button className="w-20 h-20 bg-secondary rounded-full flex items-center justify-center shadow-[0_6px_0_0] shadow-border border-4 border-border cursor-not-allowed">
              <Trophy className="w-10 h-10 text-muted-foreground" />
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
