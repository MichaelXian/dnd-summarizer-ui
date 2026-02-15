import React, { useCallback, useState } from 'react';
import { ChatHistory, MicRecorder, type ChatMessage } from '../components/chat';

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const handleMicResult = useCallback((res: { query: string; response: string }) => {
    setMessages(prev => [
      ...prev,
      { role: 'user', content: res.query },
      { role: 'assistant', content: res.response },
    ]);
  }, []);

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <h2>Chat</h2>
      <div style={{ marginBottom: '1rem' }}>
        <MicRecorder onResult={handleMicResult} />
      </div>
      <ChatHistory messages={messages} />
    </div>
  );
};

export default ChatPage;
