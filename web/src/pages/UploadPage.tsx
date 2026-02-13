import React from 'react';
import { AudioUploadContainer } from '../components/audio-upload';

const UploadPage: React.FC = () => {
  return (
    <div>
      <h2>Upload Session Audio</h2>
      <AudioUploadContainer />
    </div>
  );
};

export default UploadPage;
