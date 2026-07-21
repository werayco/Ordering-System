import './PromptCard.css'

export default function PromptCard({ text, icon: Icon, onClick }) {
  return (
    <button className="prompt-card" onClick={onClick}>
      <span className="prompt-card-text">{text}</span>
      <Icon size={16} strokeWidth={1.75} className="prompt-card-icon" />
    </button>
  )
}
