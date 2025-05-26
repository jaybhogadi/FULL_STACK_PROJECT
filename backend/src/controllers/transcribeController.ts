import { RequestHandler } from 'express';
import axios from 'axios';
import { TranscriptModel } from '../models/transcriptModel';
import { VideoModel } from '../models/videoModel';
import { TranscriptResponse } from '../types';
import { segmentTranscript } from '../utils/segmentTranscript';

export const transcribeVideoHandler: RequestHandler = async (req, res) => {
  const videoModel = (req as any).videoModel;
  const transcriptModel = (req as any).transcriptModel;

  const { filePath } = req.body;

  if (!filePath) {
    res.status(400).json({ success: false, message: 'filePath is required' });
    return;
  }

  const video = await videoModel.findByFilePath(filePath);
  if (!video) {
    res.status(404).json({ success: false, message: 'Video not found' });
    return;
  }

  try {
    const pythonResponse = await axios.post('http://localhost:5000/transcribe', { filePath });
    const transcriptText: string = pythonResponse.data.transcript;

    const segments = segmentTranscript(transcriptText);

    const transcript: TranscriptResponse = { filePath, segments };
    await transcriptModel.insert(transcript);

    res.status(200).json(transcript);
  } catch (error) {
    res.status(500).json({ success: false, message: 'Transcription failed' });
  }
};