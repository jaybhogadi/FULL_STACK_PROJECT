import { Request, Response, NextFunction, ErrorRequestHandler, RequestHandler } from 'express';
import multer from 'multer';
import { VideoModel } from '../models/videoModel';
import { UploadResponse } from '../types';

// Custom request interface (matches index.ts)
interface CustomRequest extends Request {
  videoModel?: VideoModel;
}

// Configure multer with 1 GB file size limit and destination
export const upload = multer({
  dest: 'uploads/',
  limits: { fileSize: 1 * 1024 * 1024 * 1024 }, // 1 GB
});

// Middleware to handle multer errors
export const handleMulterError: ErrorRequestHandler = (
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  if (err instanceof multer.MulterError) {
    const response: UploadResponse = {
      success: false,
      message:
        err.code === 'LIMIT_FILE_SIZE'
          ? 'File too large. Maximum size is 1 GB.'
          : `Multer error: ${err.message}`,
    };
    res.status(400).json(response);
    return;
  }

  next(err); // For non-Multer errors
};

// Upload video handler
export const uploadVideoHandler: RequestHandler = async (req: CustomRequest, res: Response) => {
  const videoModel = req.videoModel;

  console.log('Upload request received:', {
    file: req.file,
    body: req.body,
  });

  if (!req.file) {
    const response: UploadResponse = { success: false, message: 'No file uploaded or file too large' };
    res.status(400).json(response);
    return;
  }

  if (!videoModel) {
    const response: UploadResponse = { success: false, message: 'Internal server error: videoModel not found' };
    res.status(500).json(response);
    return;
  }

  try {
    const video = {
      filePath: req.file.path,
      filename: req.file.originalname,
      uploadedAt: new Date(),
    };

    console.log('Inserting video into MongoDB:', video);

    await videoModel.insert(video);

    const response: UploadResponse = {
      success: true,
      message: 'Video uploaded successfully',
      filePath: video.filePath,
    };
    

    res.status(201).json(response);
  } catch (error) {
    console.error('Error inserting video into MongoDB:', error);
    const response: UploadResponse = {
      success: false,
      message: 'Failed to save video metadata to database',
    };
    res.status(500).json(response);
  }
};
