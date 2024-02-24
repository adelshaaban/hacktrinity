import React, { useState } from 'react';
import { Button, CircularProgress, LinearProgress, Typography, Input } from '@mui/material';
import axios from 'axios';

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [videoResponse, setVideoResponse] = useState(null);
  const [imageResponse, setImageResponse] = useState(null);
  const [postureDetectionResponse, setPostureDetectionResponse] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      console.log(`Connecting to ${import.meta.env.VITE_API_URL}`)

      const response = await axios.post(import.meta.env.VITE_API_URL, formData, {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
          setUploadProgress(progress);
        },
      });

      console.log('File uploaded successfully:', response.data);

      // Check Content-Type
      const contentType = response.data.file_response.headers['content-type'];
      console.log(`Got content type of file_response = ${contentType}`)
      if (contentType.startsWith('image')) {
        // If the response is an image, display it
        console.log(`File URL = ${response.data.file_url}`)
        setVideoResponse(null);
        setImageResponse(response.data.file_url);
        setPostureDetectionResponse(response.data.verdict);
      } else if (contentType.startsWith('video')) {
        console.log(`File URL = ${response.data.file_url}`)
        setImageResponse(null);
        setVideoResponse(response.data.file_url);
        setPostureDetectionResponse(response.data.verdict);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally { 
      setIsUploading(false);
    }
  };

  if (imageResponse || videoResponse) {
    const color = postureDetectionResponse > 50 ? 'green' : 'red';
    const fontWeight = 'bold';
    return (
      <div>
        <div style={{ textAlign: 'center' }}>
          <p style={{ color, fontWeight, fontSize: '1.5rem' }}>
            Overall verdict for posture: {postureDetectionResponse.toFixed(2)}%
          </p>
          {imageResponse && <img src={imageResponse} alt="Uploaded Image" style={{ maxWidth: '100%', maxHeight: '400px' }} />}
          {videoResponse && <video controls src={videoResponse} style={{ maxWidth: '100%', maxHeight: '400px' }} />}
        </div>
      </div>
    );
  } else {
    return (
      <div>
        <div style={{ textAlign: 'center', marginTop: 20 }}>
          <Typography variant="h5">
            Upload an image or a video to detect if an alert should be sent for bad posture detection!
          </Typography>
        </div>
        <div style={{ textAlign: 'center', marginTop: 20 }}>
          <Input
            type="file"
            onChange={handleFileChange}
            disableUnderline // Removes the default underline style
            style={{ color: 'white' }} // Hide the default file input
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleUpload}
            disabled={!file || isUploading}
            style={{ marginLeft: 10, color: 'white' }}
          >
            Upload
          </Button>
          {isUploading && (
            <div style={{ marginTop: 20, maxWidth: 600, margin: '0 auto' }}>
              <CircularProgress size={24} thickness={4} />
              <Typography variant="body1" style={{ marginLeft: 10 }}>
                Uploading...
              </Typography>
            </div>
          )}
          {uploadProgress > 0 && (
            <div style={{ marginTop: 20, maxWidth: 600, margin: '0 auto' }}>
              <LinearProgress variant="determinate" value={uploadProgress} />
              <Typography variant="body1" style={{ marginTop: 5 }}>
                {uploadProgress}%
              </Typography>
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default ImageUpload;
