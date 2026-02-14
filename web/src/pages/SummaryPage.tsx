import React from 'react';
import { SummaryContainer } from '../components/summary';

const SummaryPage: React.FC = () => {
  return (
    <>
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        <h2>Summary</h2>
      </div>
      <SummaryContainer />
    </>
  );
};

export default SummaryPage;
