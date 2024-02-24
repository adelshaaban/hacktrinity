import ppLogo from '../assets/logo-white.png'
import ImageUpload from './ImageUpload'
import { Typography } from '@mui/material';
import { useEffect, useRef } from 'react';
import animBackground from 'vanta/src/vanta.globe';
import * as THREE from 'three';

const Home = () => {
  const vantaRef = useRef(null);

  useEffect(() => {
    animBackground({
      THREE: THREE,
      el: vantaRef.current,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200,
      minWidth: 200,
      backgroundColor: 0x242424,
      color: 0x242424,
    });
  }, []);

  return (
    <div ref={vantaRef} style={{ width: '100vw', height: '100vh', position: 'absolute', top: 0, left: 0 }}>
      <div style={{marginTop: 200}}>
        <Typography variant="h3">Posture Pulse</Typography>
          <div>
            <a href="" target="_blank">
              <img src={ppLogo} style={{ width: '300px', height: 'auto' }} className="logo" alt="Power Pulse logo" />
            </a>
          </div>
          <ImageUpload />
        </div>
    </div>
  );
};

export default Home;
