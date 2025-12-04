import type React from "react"
import type { Metadata } from "next"
import { Nunito } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const nunito = Nunito({ subsets: ["latin"], weight: ["400", "600", "700", "800"] })

export const metadata: Metadata = {
  title: "Handly - Learn Signing the Fun Way",
  description: "Master Sign Language through gamified lessons. Free, fun, and effective.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${nunito.className} antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
