import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import UploadPage from './pages/UploadPage'
import SummaryPage from './pages/SummaryPage'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <BrowserRouter>
      <h1>D&D Summarizer</h1>
      <Nav />
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/summary" element={<SummaryPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
