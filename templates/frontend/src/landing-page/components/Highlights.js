import React, { useState } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import { styled } from '@mui/system';

export default function Highlights() {
  const [imagesToDisplay, setImagesToDisplay] = useState([]);
  const [finalScore, setFinalScore] = useState(null);

  const StyledButtonGroup = styled(ButtonGroup)({
    marginTop: '10px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  });

  const executeScriptAndShowResults = async () => {
    try {
      const response = await axios.post('http://localhost:5000/run_deep_face_script');
      const { images_to_display, final_score } = response.data;

      // Actualizar el estado con las imágenes y el resultado
      setImagesToDisplay(images_to_display);
      setFinalScore(final_score);

      // Hacer algo con las imágenes y el resultado, por ejemplo, mostrar en la consola
      console.log('Imágenes a mostrar:', images_to_display);
      console.log('Resultado final:', final_score);
    } catch (error) {
      console.error('Error al ejecutar el script:', error);
    }
  };

  return (
    <Box
      id="highlights"
      sx={{
        pt: { xs: 4, sm: 12 },
        pb: { xs: 8, sm: 16 },
        color: 'white',
        bgcolor: '#06090a',
      }}
    >
      <Container
        sx={{
          position: 'relative',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: { xs: 3, sm: 6 },
        }}
      >
        <Box
          sx={{
            width: { sm: '100%', md: '60%' },
            textAlign: { sm: 'left', md: 'center' },
          }}
        >
          <Typography component="h2" variant="h4">
            Resultados
          </Typography>
          <Typography variant="body1" sx={{ color: 'grey.400' }}>
            A continuacion se presentan los resultados obtenidos en la grabación de la cámara.<br></br>
            Dale click al boton para obtener los resultados.
          </Typography>
        </Box>

        {/* Renderizar las imágenes y el resultado */}
        {imagesToDisplay.length > 0 && (
          <div>
            <Typography variant="h6">Imágenes a mostrar:</Typography>
            {imagesToDisplay.map((imagePath, index) => (
              <img key={index} src={`http://localhost:5000/static/${imagePath}`} alt={`Imagen ${index}`} style={{ width: '100%', marginBottom: '10px' }} />
            ))}
          </div>
        )}


        {finalScore !== null && (
          <div>
            <Typography variant="h6">Resultado final:</Typography>
            <Typography variant="body2">{finalScore}</Typography>
          </div>
        )}
        <StyledButtonGroup>
        <Button onClick={executeScriptAndShowResults}>Ejecutar Script</Button>
        </StyledButtonGroup>
      </Container>
    </Box>
  );
}
