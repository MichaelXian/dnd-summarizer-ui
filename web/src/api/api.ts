import axios from 'axios'
const BASE_URL = "http://localhost:8000";

export interface ChatResponse {
  query: string;
  response: string;
}

type AudioPayload = Blob | ArrayBuffer | Uint8Array;

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
  audio: AudioPayload
): Promise<void> => {
  await axios.post(
    `${BASE_URL}/session-audio`,
    audio,
    {
      headers: { 'Content-Type': 'application/octet-stream' },
    }
  );
}

export const postChat = async (
  audio: AudioPayload
): Promise<ChatResponse> => {
  const response = await axios.post<ChatResponse>(
    `${BASE_URL}/chat`,
    audio,
    {
      headers: { 'Content-Type': 'application/octet-stream' },
    }
  );
  return response.data;
}