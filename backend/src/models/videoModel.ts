import { MongoClient, Collection } from 'mongodb';
import { Video } from '../types';

export class VideoModel {
  private collection: Collection<Video>;

  constructor(client: MongoClient) {
    this.collection = client.db('video_transcription').collection<Video>('videos');
  }

  async insert(video: Video): Promise<void> {
    await this.collection.insertOne(video);
  }

  async findByFilePath(filePath: string): Promise<Video | null> {
    return await this.collection.findOne({ filePath });
  }
}