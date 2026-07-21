import { Plus, Search, Home, Folder, Clock, Settings } from 'lucide-react'
import './Sidebar.css'

const navItems = [
  { icon: Search, label: 'Search' },
  { icon: Home, label: 'Home' },
  { icon: Folder, label: 'Projects' },
  { icon: Clock, label: 'History' },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="logo" aria-label="App logo">
          <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
            <path d="M12 5l7 14H5l7-14z" fill="#0a0a0a" />
          </svg>
        </div>

        <button className="new-chat" aria-label="New chat">
          <Plus size={16} strokeWidth={2} />
        </button>

        <nav className="sidebar-nav" aria-label="Primary">
          {navItems.map(({ icon: Icon, label }) => (
            <button key={label} className="nav-btn" aria-label={label} title={label}>
              <Icon size={17} strokeWidth={1.75} />
            </button>
          ))}
        </nav>
      </div>

      <div className="sidebar-bottom">
        <button className="nav-btn" aria-label="Settings" title="Settings">
          <Settings size={17} strokeWidth={1.75} />
        </button>
        <button className="avatar" aria-label="Account">
          <span>UM</span>
        </button>
      </div>
    </aside>
  )
}
