import React from 'react';

export type ChatRole = 'user' | 'assistant';

export interface ChatMessage {
  role: ChatRole;
  content: string;
}

export interface ChatHistoryProps {
  messages: ChatMessage[];
  emptyText?: string;
  style?: React.CSSProperties;
}

const bubbleColor: Record<ChatRole, string> = {
  user: '#e8f0fe',
  assistant: '#f6f6f6',
};

const alignSelf: Record<ChatRole, 'flex-end' | 'flex-start'> = {
  user: 'flex-end',
  assistant: 'flex-start',
};

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, emptyText = 'No messages yet.', style }) => {
  return (
    <div style={{
      maxWidth: 800,
      backgroundColor: '#fff',
      borderRadius: 8,
      padding: '1rem',
      margin: '0 auto',
      textAlign: 'left',
      ...style,
    }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
      }}>
        {messages.length === 0 && (
          <div style={{ color: '#666', fontStyle: 'italic' }}>{emptyText}</div>
        )}
        {messages.map((m, idx) => {
          const key = idx;
          const role = m.role;
          return (
            <div key={key} style={{ display: 'flex'}}>
              <div
                style={{
                  alignSelf: alignSelf[role],
                  background: bubbleColor[role],
                  padding: '0.6rem 0.8rem',
                  borderRadius: 10,
                  maxWidth: '80%',
                  whiteSpace: 'pre-wrap',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.06)'
                }}
              >
                <div style={{ fontSize: 12, color: '#666', marginBottom: 4, textTransform: 'capitalize' }}>
                  {role}
                </div>
                <div style={{ color: '#111' }}>{m.content}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ChatHistory;
