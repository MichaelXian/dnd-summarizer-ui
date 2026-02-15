import React, { useCallback, useEffect, useRef, useState } from 'react';
import { postChat, type ChatResponse } from '../../api/api';

export interface MicRecorderProps {
  onResult?: (result: ChatResponse) => void;
}

const MicRecorder: React.FC<MicRecorderProps> = ({ onResult }) => {
  const [supported, setSupported] = useState<boolean>(true);
  const [recording, setRecording] = useState<boolean>(false);
  const [uploading, setUploading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ChatResponse | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);

  useEffect(() => {
    // Capability check
    const ok = !!(navigator.mediaDevices && window.MediaRecorder);
    setSupported(ok);
  }, []);

  const cleanupStream = () => {
    if (mediaRecorderRef.current) {
      try {
        if (mediaRecorderRef.current.state !== 'inactive') {
          mediaRecorderRef.current.stop();
        }
      } catch {}
      mediaRecorderRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
  };

  useEffect(() => {
    return () => cleanupStream();
  }, []);

  const startRecording = useCallback(async () => {
    setError(null);
    setResult(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const mimeTypes = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/ogg;codecs=opus',
        'audio/ogg'
      ];
      let mimeType = '';
      for (const mt of mimeTypes) {
        if ((window as any).MediaRecorder && MediaRecorder.isTypeSupported(mt)) {
          mimeType = mt;
          break;
        }
      }

      const mr = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      mediaRecorderRef.current = mr;
      chunksRef.current = [];

      mr.ondataavailable = (e: BlobEvent) => {
        if (e.data && e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mr.onstop = async () => {
        try {
          const blob = new Blob(chunksRef.current, { type: mr.mimeType || 'audio/webm' });
          chunksRef.current = [];
          setUploading(true);
          const resp = await postChat(blob);
          if (onResult) {
            onResult(resp);
          } else {
            setResult(resp);
          }
        } catch (e: any) {
          const message = e?.response?.data?.message || e?.message || 'Upload failed';
          setError(message);
        } finally {
          setUploading(false);
        }
      };

      mr.start();
      setRecording(true);
    } catch (e: any) {
      const message = e?.message || 'Microphone access failed';
      setError(message);
      cleanupStream();
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (!mediaRecorderRef.current) return;
    try {
      if (mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    } catch (e) {
      // ignore
    } finally {
      setRecording(false);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
        streamRef.current = null;
      }
    }
  }, []);

  if (!supported) {
    return <div style={{ color: '#b00' }}>Your browser does not support microphone recording.</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', alignItems: 'center' }}>
      <button
        onClick={recording ? stopRecording : startRecording}
        disabled={uploading}
        style={{
          minWidth: 180,
          padding: '0.75rem 1.25rem',
          borderRadius: 999,
          border: '1px solid #ccc',
          background: recording ? '#ffeaea' : '#eef7ff',
          color: '#111',
          cursor: uploading ? 'not-allowed' : 'pointer',
          fontWeight: 600
        }}
      >
        {recording ? 'Stop recording' : 'Start recording'}
      </button>
      {recording && <div style={{ color: '#b00' }}>Recording…</div>}
      {uploading && <div>Uploading…</div>}
      {error && <div style={{ color: 'crimson' }}>{error}</div>}
      {result && (
        <div style={{ width: '100%', maxWidth: 800, textAlign: 'left' }}>
          <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Transcribed query</div>
          <div style={{ background: '#f6f6f6', padding: '0.75rem', borderRadius: 8, marginBottom: '0.5rem' }}>
            {result.query}
          </div>
          <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Response</div>
          <div style={{ background: '#f6f6f6', padding: '0.75rem', borderRadius: 8 }}>
            {result.response}
          </div>
        </div>
      )}
    </div>
  );
};

export default MicRecorder;
