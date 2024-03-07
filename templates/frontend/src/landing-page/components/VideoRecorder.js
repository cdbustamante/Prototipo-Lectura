import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import Box from '@mui/material/Box';
import { styled } from '@mui/system';
import Swal from 'sweetalert2';

const StyledVideo = styled('video')({
  width: '1100px',
  height: '600px',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  maxWidth: '100%',
  maxHeight: '100%',
  border: '1px solid #ddd',
  borderRadius: '5px',
});

const StyledButtonGroup = styled(ButtonGroup)({
  marginTop: '10px',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
});

const VideoRecorder = () => {
  const videoRef = useRef(null);
  const [recording, setRecording] = useState(false);

  useEffect(() => {
    const initializeCamera = async () => {
      try {
        // Acceder a la cámara y actualizar el video en tiempo real
        const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = mediaStream;
      } catch (error) {
        console.error('Error initializing camera:', error);
      }
    };

    initializeCamera();

    return () => {
      // Limpiar cualquier recurso o suscripción si es necesario
    };
  }, []); // Usar un array vacío para que se ejecute solo una vez al montar el componente

  const showConfirmationAlert = async () => {
    const result = await Swal.fire({
      title: '¿Estás seguro de iniciar la grabación?',
      text: 'No podrás revertir esto.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, estoy de acuerdo',
      cancelButtonText: 'No, cancelar',
    });

    if (result.isConfirmed) {
      startRecording();
    }
  };

  const startRecording = async () => {
    try {
      await axios.post('http://localhost:5000/start_recording');
      setRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = async () => {
    try {
      await axios.post('http://localhost:5000/stop_recording');
      setRecording(false);
    } catch (error) {
      console.error('Error stopping recording:', error);
    }
  };

  return (
    <Box>
      <StyledVideo ref={videoRef} controls autoPlay />
      <StyledButtonGroup size="small" aria-label="Small button group">
        <Button onClick={showConfirmationAlert} disabled={recording}>
          Iniciar Grabación
        </Button>
        <Button onClick={stopRecording} disabled={!recording}>
          Detener Grabación
        </Button>
      </StyledButtonGroup>
    </Box>
  );
};

export default VideoRecorder;
