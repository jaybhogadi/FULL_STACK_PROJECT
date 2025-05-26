import cors from 'cors';
import express, { Request, Response, NextFunction } from 'express';
import { MongoClient } from 'mongodb';
import { VideoModel } from './models/videoModel';
import { TranscriptModel } from './models/transcriptModel';
import { QuestionModel } from './models/questionModel';
import { upload, uploadVideoHandler } from './controllers/uploadController';
import { transcribeVideoHandler } from './controllers/transcribeController';
import { generateQuestionsHandler, updateQuestionHandler } from './controllers/questionController';
import dotenv from 'dotenv';
dotenv.config(); // Load variables from .env into process.env

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json()); // Remove duplicate

const user = process.env.MONGO_USER;
const password = process.env.MONGO_PASSWORD;
const cluster = process.env.MONGO_CLUSTER;


const uri = `mongodb+srv://${user}:${password}@${cluster}/video_transcription?retryWrites=true&w=majority&appName=Cluster0`; 
const client = new MongoClient(uri);

// Middleware to attach models to request
interface CustomRequest extends Request {
  videoModel?: VideoModel;
  transcriptModel?: TranscriptModel;
  questionModel?: QuestionModel;
}

const attachModels = (
  videoModel: VideoModel,
  transcriptModel: TranscriptModel,
  questionModel: QuestionModel
) => (req: CustomRequest, res: Response, next: NextFunction) => {
  req.videoModel = videoModel;
  req.transcriptModel = transcriptModel;
  req.questionModel = questionModel;
  next();
};


async function startServer() {
  try {
    // await client.connect();
    console.log('Connected to MongoDB Atlas');

    const videoModel = new VideoModel(client);
    const transcriptModel = new TranscriptModel(client);
    const questionModel = new QuestionModel(client);

    // Attach models to all routes
    app.use(attachModels(videoModel, transcriptModel, questionModel));

    // Routes
    app.post('/upload', upload.single('video'), uploadVideoHandler);
    app.post('/transcribe', transcribeVideoHandler);
    app.post('/generate-questions', generateQuestionsHandler);
    app.put('/update-question', updateQuestionHandler); // Optional



    app.listen(port, () => {
      console.log(`Server running on http://localhost:${port}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();