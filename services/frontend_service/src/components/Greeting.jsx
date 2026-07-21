import './Greeting.css'

export default function Greeting({ name }) {
  return (
    <header className="greeting">
      <h1 className="greeting-title">
        <span className="greeting-line greeting-line--dim">Hi there, {name}</span>
        <span className="greeting-line greeting-line--bright">
          What would like to know?
        </span>
      </h1>
      <p className="greeting-sub">
        Use one of the most common prompts
        <br />
        below or use your own to begin
      </p>
    </header>
  )
}
