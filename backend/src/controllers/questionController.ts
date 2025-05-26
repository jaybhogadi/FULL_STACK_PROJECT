import { RequestHandler } from 'express';
import axios from 'axios';
import { QuestionModel } from '../models/questionModel';
import { TranscriptModel } from '../models/transcriptModel';
import { MCQResponse, MCQ, MCQOption } from '../types';

export const generateQuestionsHandler: RequestHandler = async (req, res) => {
  const transcriptModel = (req as any).transcriptModel;
  const questionModel = (req as any).questionModel;

  const { segment, segmentId, filePath } = req.body;

  if (!segment || !segmentId || !filePath) {
    res.status(400).json({ success: false, message: 'segment, segmentId, and filePath are required' });
    return;
  }

  const transcript = await transcriptModel.findByFilePath(filePath);
  if (!transcript) {
    res.status(404).json({ success: false, message: 'Transcript not found' });
    return;
  }

  try {
    const pythonResponse = await axios.post('http://localhost:5000/generate-mcq', { segment });
    const pythonQuestions: { question: string; options: string[]; correctAnswer: string }[] = pythonResponse.data.questions;

    const questions: MCQ[] = pythonQuestions.map((q, index) => ({
      id: `${segmentId}-${index}`,
      question: q.question,
      options: q.options.map((opt, optIndex) => ({ id: `${segmentId}-${index}-${optIndex}`, text: opt })),
      correctAnswer: q.correctAnswer,
      segmentId,
    }));

    const mcqResponse: MCQResponse = { filePath, segmentId, questions };
    await questionModel.insert(mcqResponse);

    res.status(200).json(mcqResponse);
  } catch (error) {
    res.status(500).json({ success: false, message: 'Question generation failed' });
  }
};

export const updateQuestionHandler: RequestHandler = async (req, res) => {
  const questionModel = (req as any).questionModel;

  const { segmentId, updatedQuestion } = req.body;

  if (!segmentId || !updatedQuestion) {
    res.status(400).json({ success: false, message: 'segmentId and updatedQuestion are required' });
    return;
  }

  await questionModel.updateQuestion(segmentId, updatedQuestion);
  res.status(200).json({ success: true, message: 'Question updated', updatedQuestion });
};