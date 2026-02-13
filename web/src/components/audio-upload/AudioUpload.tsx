import React from 'react';

export interface AudioUploadProps {
  onFileChange: (file: Blob | null) => void;
  onUpload: () => void;
  loading?: boolean;
  error?: string | null;
  success?: boolean;
  selectedFile?: Blob | null;
}

const AudioUpload: React.FC<AudioUploadProps> = ({
  onFileChange,
  onUpload,
  loading = false,
  error = null,
  success = false,
  selectedFile = null,
}) => {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files && e.target.files.length > 0 ? e.target.files[0] : null;
    onFileChange(file);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'center' }}>
      <input
        type="file"
        accept="audio/*"
        onChange={handleInputChange}
        disabled={loading}
      />
      <button onClick={onUpload} disabled={loading || !selectedFile}>
        {loading ? 'Uploading…' : 'Upload audio'}
      </button>
      {error && <div style={{ color: 'crimson' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>Upload complete.</div>}
    </div>
  );
};

export default AudioUpload;
