import React, { useState } from 'react';
import { Button, CircularProgress, LinearProgress, Typography } from '@mui/material';
import axios from 'axios';

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [videoResponse, setVideoResponse] = useState(null);
  const [imageResponse, setImageResponse] = useState(null);
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

      const response = await axios.post('http://172.20.10.3:8000/api', formData, {
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
        console.log(response.data.file_url)
        setImageResponse(response.data.file_url);
      } else if (contentType.startsWith('video')) {
        console.log(response.data.file_url)
        setVideoResponse(response.data.file_url);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div>
      <div style={{ textAlign: 'center', marginTop: 20 }}>
        <Typography variant="h5">Power Pulse</Typography>
        <Typography variant="body1">
          Upload an image or a video to detect if an alert should be sent for bad posture detection!
        </Typography>
      </div>
      <div style={{ textAlign: 'center', marginTop: 20 }}>
        <input
          type="file"
          onChange={handleFileChange}
          style={{
            color: 'white',
          }}
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
          <div style={{ marginTop: 20 }}>
            <CircularProgress size={24} thickness={4} />
            <Typography variant="body1" style={{ marginLeft: 10 }}>
              Uploading...
            </Typography>
          </div>
        )}
        {uploadProgress > 0 && (
          <div style={{ marginTop: 20 }}>
            <LinearProgress variant="determinate" value={uploadProgress} />
            <Typography variant="body1" style={{ marginTop: 5 }}>
              {uploadProgress}%
            </Typography>
          </div>
        )}
      </div>
      <div style={{ textAlign: 'center', marginTop: 20 }}>
        {imageResponse && <img src={imageResponse} alt="Uploaded Image" style={{ maxWidth: '100%', maxHeight: '400px' }} />}
        {videoResponse && <video controls src={videoResponse} style={{ maxWidth: '100%', maxHeight: '400px' }} />}
      </div>
    </div>
  );
}

export default ImageUpload;
