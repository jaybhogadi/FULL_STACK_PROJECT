import { TranscriptSegment } from '../types';
import { v4 as uuidv4 } from 'uuid';

export const segmentTranscript = (transcript: string, fileDuration: number = 120): TranscriptSegment[] => {
  // Simplified for MVP: Split into two equal parts (assuming 2-minute video for testing)
  const words = transcript.split(' ');
  const midPoint = Math.floor(words.length / 2);
  const segmentDuration = fileDuration / 2; // e.g., 60 seconds per segment

  const segments: TranscriptSegment[] = [
    {
      id: uuidv4(),
      text: words.slice(0, midPoint).join(' '),
      startTime: 0,
      endTime: segmentDuration,
      timeRange: `00:00 - ${formatTime(segmentDuration)}`,
    },
    {
      id: uuidv4(),
      text: words.slice(midPoint).join(' '),
      startTime: segmentDuration,
      endTime: fileDuration,
      timeRange: `${formatTime(segmentDuration)} - ${formatTime(fileDuration)}`,
    },
  ];

  return segments;
};

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
  const secs = (seconds % 60).toString().padStart(2, '0');
  return `${mins}:${secs}`;
};