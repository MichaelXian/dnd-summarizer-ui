import React from 'react';
import { ChatHistory } from '../components/chat';

const ChatPage: React.FC = () => {

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <h2>Chat</h2>
      <ChatHistory messages={[]} />
    </div>
  );
};

export default ChatPage;
