import { Hand } from "lucide-react"

export function Footer() {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Hand className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-extrabold text-foreground">Handly</span>
          </div>

          <nav className="flex flex-wrap items-center justify-center gap-6">
            <a href="#" className="text-muted-foreground hover:text-foreground font-semibold transition-colors">
              About
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground font-semibold transition-colors">
              Blog
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground font-semibold transition-colors">
              Careers
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground font-semibold transition-colors">
              Privacy
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground font-semibold transition-colors">
              Terms
            </a>
          </nav>

          <p className="text-muted-foreground text-sm">© 2025 Handly. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
