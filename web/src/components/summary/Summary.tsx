import React from 'react';

export interface SummaryProps {
  summary: string;
  loading?: boolean;
}

const Summary: React.FC<SummaryProps> = ({ summary, loading = false }) => {
  return (
    <div style={{ maxWidth: 800, margin: '0 auto', color: '#111' }}>
      <pre style={{ whiteSpace: 'pre-wrap', background: '#f6f6f6', color: '#111', padding: '1rem', borderRadius: 8 }}>
        {summary || (loading ? 'Loading…' : 'No summary available yet.')}
      </pre>
    </div>
  );
};

export default Summary;
