export interface UserData {
  name: string
  xp: number
  level: number
  levelProgress: number
  streak: number
  completedLessons: number[]
}

const DEFAULT_USER: UserData = {
  name: "Alex",
  xp: 1250,
  level: 5,
  levelProgress: 65,
  streak: 5,
  completedLessons: [],
}

const STORAGE_KEY = "handly_user"

export function getUserData(): UserData {
  if (typeof window === "undefined") return DEFAULT_USER

  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_USER))
    return DEFAULT_USER
  }
  return JSON.parse(stored)
}

export function updateUserData(updates: Partial<UserData>): UserData {
  const current = getUserData()
  const updated = { ...current, ...updates }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  return updated
}

export function completeLesson(lessonId: number, xpGained: number): UserData {
  const current = getUserData()

  // Add lesson to completed if not already
  const completedLessons = current.completedLessons.includes(lessonId)
    ? current.completedLessons
    : [...current.completedLessons, lessonId]

  // Update XP and level progress
  const newXp = current.xp + xpGained
  let newLevel = current.level
  let newLevelProgress = current.levelProgress + 6 // ~6% per lesson

  // Level up if progress hits 100
  if (newLevelProgress >= 100) {
    newLevel += 1
    newLevelProgress = newLevelProgress - 100
  }

  // Increment streak
  const newStreak = current.streak + 1

  return updateUserData({
    xp: newXp,
    level: newLevel,
    levelProgress: newLevelProgress,
    streak: newStreak,
    completedLessons,
  })
}

export function resetUserData(): UserData {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_USER))
  return DEFAULT_USER
}
