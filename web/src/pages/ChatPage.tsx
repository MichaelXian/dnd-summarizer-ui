import React from 'react';
import { ChatHistory, MicRecorder } from '../components/chat';

const ChatPage: React.FC = () => {
  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <h2>Chat</h2>
      <div style={{ marginBottom: '1rem' }}>
        <MicRecorder />
      </div>
      <ChatHistory messages={[]} />
    </div>
  );
};

export default ChatPage;
