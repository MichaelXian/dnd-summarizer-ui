import React, { useEffect, useRef, useState } from 'react';
import { getSummary } from '../../api/api';
import Summary from './Summary';

const RETRY_DELAY_MS = 2000;

const SummaryContainer: React.FC = () => {
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const retryTimeoutRef = useRef<number | null>(null);
  const stoppedRef = useRef<boolean>(false);

  useEffect(() => {
    let active = true;

    const attempt = async () => {
      if (!active || stoppedRef.current) return;
      setLoading(true);
      try {
        const text = await getSummary();
        if (!active) return;
        setSummary(text);
        setLoading(false);
        stoppedRef.current = true; // stop further retries on success
      } catch (e: any) {
        if (!active) return;
        // schedule another attempt
        retryTimeoutRef.current = window.setTimeout(() => {
          attempt();
        }, RETRY_DELAY_MS) as unknown as number;
      }
    };

    // initial attempt
    attempt();

    return () => {
      active = false;
      if (retryTimeoutRef.current) {
        window.clearTimeout(retryTimeoutRef.current);
        retryTimeoutRef.current = null;
      }
    };
  }, []);

  return (
    <Summary summary={summary} loading={loading}/>
  );
};

export default SummaryContainer;
