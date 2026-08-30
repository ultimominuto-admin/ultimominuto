
    const express = require('express');
const cors = require('cors');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();

// Configuración de Gemini IA
const ai = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || 'api_key_placeholder');

app.use(express.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// ENDPOINT GENERADOR DE CV CON IA
app.post('/api/generate-cv', async (req, res) => {
  try {
    const { currentCv, targetRole, language } = req.body;
    
    if (!currentCv) {
      return res.status(400).json({ success: false, error: 'El contenido del CV es obligatorio.' });
    }

    const prompt = `Actúa como un reclutador experto. Optimiza el siguiente borrador/experiencia de CV para superar los filtros ATS para el puesto objetivo: "${targetRole || 'Profesional'}".
Idioma de respuesta: ${language || 'Español'}.

Borrador/Experiencia introducida:
${currentCv}

Devuelve un HTML limpio estructurado con etiquetas h2, h3, p, ul, li para renderizar un CV profesional. No incluyas marcas de código markdown ni bloques de triple comilla (```html).`;

    const model = ai.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    const response = await result.response;

    res.json({ success: true, cvHtml: response.text() });
  } catch (error) {
    console.error('Error en /api/generate-cv:', error);
    res.status(500).json({ success: false, error: 'Error al procesar el CV con la IA.' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor de Cvminuto activo en puerto ${PORT}`));
