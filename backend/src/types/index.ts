// Represents a segment of the transcript (5-minute chunk)
export interface TranscriptSegment {
  id: string;
  text: string;
  startTime: number; // e.g., 0 (seconds)
  endTime: number;   // e.g., 300 (seconds)
  timeRange: string; // e.g., "00:00 - 05:00"
}

// Represents an option for an MCQ
export interface MCQOption {
  id: string;
  text: string;
}

// Represents a multiple-choice question
export interface MCQ {
  id: string;
  question: string;
  options: MCQOption[];
  correctAnswer: string;
  segmentId: string; // Links to a TranscriptSegment
}

// Response for the /upload endpoint
export interface UploadResponse {
  success: boolean;
  message: string;
  filePath?: string; // e.g., "uploads/video123.mp4"
}

// Response for the /transcribe endpoint
export interface TranscriptResponse {
  filePath: string;
  segments: TranscriptSegment[];
}

// Response for the /generate-questions endpoint
export interface MCQResponse {
  filePath: string;
  segmentId: string;
  questions: MCQ[];
}

// (Optional) Response for the /update-question endpoint
export interface UpdateQuestionResponse {
  success: boolean;
  message: string;
  updatedQuestion: MCQ;
}

// MongoDB document for videos
export interface Video {
  _id?: string;
  filePath: string;
  filename: string;
  uploadedAt: Date;
}

// MongoDB document for transcripts
export interface Transcript {
  _id?: string;
  filePath: string;
  segments: TranscriptSegment[];
}

// MongoDB document for MCQs
export interface QuestionSet {
  _id?: string;
  filePath: string;
  segmentId: string;
  questions: MCQ[];
}