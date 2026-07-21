import { useState } from 'react'
import {
  User,
  Mail,
  Camera,
  SlidersHorizontal,
  RefreshCw,
  ListTodo,
  Globe,
  Lightbulb,
  Code2,
} from 'lucide-react'
import PromptCard from './PromptCard.jsx'
import './PromptGrid.css'

const promptSets = [
  [
    { text: 'Write a to-do list for a personal project or task', icon: User },
    { text: 'Generate an email to reply to a job offer', icon: Mail },
    { text: 'Summarise this article or text for me in one paragraph', icon: Camera },
    { text: 'How does AI work in a technical capacity', icon: SlidersHorizontal },
  ],
  [
    { text: 'Plan a weekly schedule that balances work and rest', icon: ListTodo },
    { text: 'Explain a complex topic like I am five years old', icon: Lightbulb },
    { text: 'Draft a short bio for my professional profile', icon: Globe },
    { text: 'Review this code snippet and suggest improvements', icon: Code2 },
  ],
]

export default function PromptGrid({ onSelectPrompt }) {
  const [setIndex, setSetIndex] = useState(0)
  const [spinning, setSpinning] = useState(false)

  const refresh = () => {
    setSpinning(true)
    setSetIndex((i) => (i + 1) % promptSets.length)
    setTimeout(() => setSpinning(false), 450)
  }

  return (
    <section className="prompt-section" aria-label="Suggested prompts">
      <div className="prompt-grid">
        {promptSets[setIndex].map((prompt) => (
          <PromptCard
            key={prompt.text}
            text={prompt.text}
            icon={prompt.icon}
            onClick={() => onSelectPrompt(prompt.text)}
          />
        ))}
      </div>

      <button className="refresh-btn" onClick={refresh}>
        <RefreshCw size={13} strokeWidth={1.75} className={spinning ? 'spin' : ''} />
        Refresh Prompts
      </button>
    </section>
  )
}
