const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve the serialized model file
app.get('/download/model', (req, res) => {
    const modelPath = path.join(__dirname, 'models', 'serialized_model.pkl');
    res.download(modelPath);
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    const url = `http://localhost:${PORT}`;
    console.log(`Server is running at ${url}`);
    console.log(`You can access the webpage at ${url}`);
});
