import React, { useState, useCallback } from 'react';
import { uploadSessionAudio } from '../../api/api';
import AudioUpload from './AudioUpload';

const AudioUploadContainer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<Blob | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const onFileChange = useCallback((file: Blob | null) => {
    setSelectedFile(file);
    setError(null);
    setSuccess(false);
  }, []);

  const onUpload = useCallback(async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      await uploadSessionAudio(selectedFile);
      setSuccess(true);
    } catch (e: any) {
      const message = e?.response?.data?.message || e?.message || 'Upload failed';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [selectedFile]);

  return (
    <AudioUpload
      onFileChange={onFileChange}
      onUpload={onUpload}
      loading={loading}
      error={error}
      success={success}
      selectedFile={selectedFile}
    />
  );
};

export default AudioUploadContainer;
