export type CandidateBook = {
  title: string;
  snippet: string;
  score: number;
};

export type ChatRequest = {
  message: string;
  k?: number;
};

export type ChatResponse = {
  recommendation: string;
  summary: string;
  reason: string;
  candidates: CandidateBook[];
};