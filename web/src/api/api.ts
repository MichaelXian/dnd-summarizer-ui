import axios from 'axios'
const BASE_URL = "http://localhost:8000";

export interface ChatResponse {
  query: string;
  response: string;
}

export const getTranscript = async (): Promise<string> => {
  const response = await axios.get<string>(
    `${BASE_URL}/transcript`,
    { responseType: 'text' as const }
  );
  return response.data;
};

export const getSummary = async (): Promise<string> => {
  const response = await axios.get<string>(
    `${BASE_URL}/summary`,
    { responseType: 'text' as const }
  );
  return response.data;
};

export const uploadSessionAudio = async (
  audio: Blob,
  filename = 'audio.webm'
): Promise<void> => {
  const formData = new FormData();
  // Provide a filename to ensure proper handling when passing a generic Blob
  formData.append("file", audio, filename);
  await axios.post(
    `${BASE_URL}/session-audio`,
    formData
    // Let Axios set the correct multipart/form-data boundary automatically
  );
}

export const postChat = async (
  audio: Blob,
): Promise<ChatResponse> => {
  const formData = new FormData();
  formData.append("file", audio, (audio as any)?.name ?? 'audio.webm');
  const response = await axios.post<ChatResponse>(
    `${BASE_URL}/chat`,
    formData
  );
  return response.data;
}