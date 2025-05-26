import { MongoClient, Collection } from 'mongodb';
import { QuestionSet } from '../types';

export class QuestionModel {
  private collection: Collection<QuestionSet>;

  constructor(client: MongoClient) {
    this.collection = client.db('video_transcription').collection<QuestionSet>('questions');
  }

  async insert(questionSet: QuestionSet): Promise<void> {
    await this.collection.insertOne(questionSet);
  }

  async findBySegmentId(segmentId: string): Promise<QuestionSet | null> {
    return await this.collection.findOne({ segmentId });
  }

  async updateQuestion(segmentId: string, updatedQuestion: QuestionSet['questions'][0]): Promise<void> {
    await this.collection.updateOne(
      { segmentId, 'questions.id': updatedQuestion.id },
      { $set: { 'questions.$': updatedQuestion } }
    );
  }
}