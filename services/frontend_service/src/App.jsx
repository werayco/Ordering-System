import { useState } from 'react'
import Sidebar from './components/Sidebar.jsx'
import Greeting from './components/Greeting.jsx'
import PromptGrid from './components/PromptGrid.jsx'
import ChatInput from './components/ChatInput.jsx'

export default function App() {
  const [inputValue, setInputValue] = useState('')

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <div className="main-inner">
          <Greeting name="Ui Mahadi" />
          <PromptGrid onSelectPrompt={setInputValue} />
          <ChatInput value={inputValue} onChange={setInputValue} />
        </div>
      </main>
    </div>
  )
}
