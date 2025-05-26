import { MongoClient, Collection } from 'mongodb';
import { Transcript } from '../types';

export class TranscriptModel {
  private collection: Collection<Transcript>;

  constructor(client: MongoClient) {
    this.collection = client.db('video_transcription').collection<Transcript>('transcripts');
  }

  async insert(transcript: Transcript): Promise<void> {
    await this.collection.insertOne(transcript);
  }

  async findByFilePath(filePath: string): Promise<Transcript | null> {
    return await this.collection.findOne({ filePath });
  }
}