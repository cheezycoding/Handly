"use client"

import { Hand, Flame, User } from "lucide-react"
import Link from "next/link"
import { useEffect, useState } from "react"
import { getUserData, type UserData } from "@/lib/user-store"

export function Header() {
  const [user, setUser] = useState<UserData | null>(null)

  useEffect(() => {
    setUser(getUserData())

    // Listen for storage changes to update in real-time
    const handleStorage = () => setUser(getUserData())
    window.addEventListener("storage", handleStorage)
    return () => window.removeEventListener("storage", handleStorage)
  }, [])

  // Show placeholder while loading
  if (!user) {
    return (
      <header className="sticky top-0 z-50 bg-background border-b border-border">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
              <Hand className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="text-2xl font-extrabold text-foreground">Handly</span>
          </Link>
        </div>
      </header>
    )
  }

  return (
    <header className="sticky top-0 z-50 bg-background border-b border-border">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
            <Hand className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="text-2xl font-extrabold text-foreground">Handly</span>
        </Link>

        <div className="flex items-center gap-4">
          {/* Streak */}
          <div className="flex items-center gap-1.5 bg-card px-3 py-1.5 rounded-xl border-2 border-border">
            <Flame className="w-5 h-5 text-orange-500" />
            <span className="font-bold text-foreground">{user.streak}</span>
          </div>

          {/* XP and Level */}
          <div className="flex items-center gap-3 bg-card px-3 py-1.5 rounded-xl border-2 border-border">
            <div className="flex flex-col items-end">
              <span className="text-xs text-muted-foreground font-semibold">LEVEL {user.level}</span>
              <div className="w-20 h-2 bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-primary rounded-full" style={{ width: `${user.levelProgress}%` }} />
              </div>
            </div>
            <span className="font-bold text-accent">{user.xp} XP</span>
          </div>

          {/* Profile avatar */}
          <button className="w-10 h-10 bg-primary rounded-full flex items-center justify-center border-2 border-primary hover:border-primary/70 transition-colors">
            <User className="w-5 h-5 text-primary-foreground" />
          </button>
        </div>
      </div>
    </header>
  )
}
