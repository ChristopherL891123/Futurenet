const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const UPLOADS_DIR = path.join(__dirname, 'uploads');

// Ensure the uploads directory exists
fs.mkdirSync(UPLOADS_DIR, { recursive: true });

// Middleware to parse JSON and URL-encoded bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Multer configuration for file uploads
const upload = multer({ dest: UPLOADS_DIR });

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Define a route handler for the root route ("/")
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Endpoint to receive CSV file, serialized pickle model, and column names
app.post('/retrain', upload.fields([{ name: 'csv' }, { name: 'model' }]), async (req, res) => {
  try {
    const { columns } = req.body;

    // Validate files and columns are received
    if (!req.files || !req.files['csv'] || !req.files['model'] || !columns) {
      res.status(400).send('Missing files or columns');
      return;
    }

    // Save CSV and model files in the 'uploads' directory
    const csvFilePath = req.files['csv'][0].path;
    const modelFilePath = req.files['model'][0].path;

    // Construct the path to the Python script in the 'public' directory
    const pythonScriptPath = path.join(__dirname, 'public', 'retrain_script.py');

    // Construct the command to execute the Python script with arguments
    const command = `python "${pythonScriptPath}" "${columns}"`;

    // Execute the command
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        res.status(500).send('Internal Server Error');
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);

      try {
        // Read serialized retrained model from file
        const retrainedModelPath = path.join(UPLOADS_DIR, 'retrained_model.pkl');
        const retrainedModel = fs.readFileSync(retrainedModelPath);

        // Send the serialized retrained model back to the user
        res.send(retrainedModel);
      } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
      }
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
