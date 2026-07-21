import { useEffect, useRef, useState } from 'react'
import {
  Globe,
  ChevronDown,
  CirclePlus,
  Image,
  ArrowRight,
  Check,
} from 'lucide-react'
import './ChatInput.css'

const MAX_CHARS = 1000
const scopes = ['All Web', 'Academic', 'News', 'Social']

export default function ChatInput({ value, onChange }) {
  const [scope, setScope] = useState(scopes[0])
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    const close = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', close)
    return () => document.removeEventListener('mousedown', close)
  }, [])

  const handleInput = (e) => {
    onChange(e.target.value.slice(0, MAX_CHARS))
  }

  const handleSend = () => {
    if (!value.trim()) return
    // Hook your submit logic here
    console.log('Sending:', { scope, message: value })
    onChange('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <section className="chat-input" aria-label="Message input">
      <div className="chat-input-top">
        <textarea
          className="chat-textarea"
          placeholder="Ask whatever you want..."
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          rows={2}
          aria-label="Ask whatever you want"
        />

        <div className="scope" ref={menuRef}>
          <button
            className="scope-btn"
            onClick={() => setMenuOpen((o) => !o)}
            aria-haspopup="listbox"
            aria-expanded={menuOpen}
          >
            <Globe size={13} strokeWidth={1.75} />
            {scope}
            <ChevronDown size={13} strokeWidth={1.75} className="scope-chevron" />
          </button>

          {menuOpen && (
            <ul className="scope-menu" role="listbox" aria-label="Search scope">
              {scopes.map((s) => (
                <li key={s}>
                  <button
                    className={`scope-option ${s === scope ? 'active' : ''}`}
                    role="option"
                    aria-selected={s === scope}
                    onClick={() => {
                      setScope(s)
                      setMenuOpen(false)
                    }}
                  >
                    {s}
                    {s === scope && <Check size={12} strokeWidth={2} />}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="chat-input-bottom">
        <div className="chat-actions">
          <button className="action-btn">
            <CirclePlus size={15} strokeWidth={1.75} />
            Add Attachment
          </button>
          <button className="action-btn">
            <Image size={15} strokeWidth={1.75} />
            Use Image
          </button>
        </div>

        <div className="chat-meta">
          <span className="char-count">
            {value.length}/{MAX_CHARS}
          </span>
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!value.trim()}
            aria-label="Send message"
          >
            <ArrowRight size={15} strokeWidth={2} />
          </button>
        </div>
      </div>
    </section>
  )
}
