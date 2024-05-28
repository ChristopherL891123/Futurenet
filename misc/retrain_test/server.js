const express = require('express');
const multer = require('multer');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');

const app = express();
const port = 3000;

// Setup for handling file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname)
    }
});
const upload = multer({ storage: storage });



// Serve the HTML form
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/index.html'));
});

// Handle file data upload and initiate model training
app.post('/upload', upload.single('dataset'), (req, res) => {
    // Load the model record from JSON
    const modelRecordPath = path.join(__dirname, 'model_record.json');
    let modelRecord = {};
    if (fs.existsSync(modelRecordPath)) {
        modelRecord = JSON.parse(fs.readFileSync(modelRecordPath, 'utf8'));
    }
    
    const model_name = req.body.modelName;
    const dataset_path = path.join(__dirname, 'uploads', req.file.filename);
    const target_variable = req.body.targetVariable;

    // Retrieve model identifier from JSON or use a default value
    const model_identifier = modelRecord[model_name] ;
    const model_filename = `${model_name}_${model_identifier}.pkl`;  // Updated filename with underscore and identifier

    const execCommand = `python "${model_name}.py" "${dataset_path}" "${target_variable}"`;

    exec(execCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(`Error training model: ${stderr}`);
        }
        // Updated the response to include the correct filename in the download link
        res.send(`Model trained successfully! <a href="/download/${model_filename}">Download Model</a>`);
    });
});

// Route to download the model file
app.get('/download/:filename', (req, res) => {
    const filename = req.params.filename;
    const filepath = path.join(__dirname, 'uploads', filename); // Ensure to look in the correct directory
    if (fs.existsSync(filepath)) {
        res.download(filepath); // Provide the file for download
    } else {
        res.status(404).send('File not found');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});



















// const express = require('express');
// const multer = require('multer');
// const path = require('path');
// const { exec } = require('child_process');
// const fs = require('fs');

// const app = express();
// const port = 3000;

// // Setup for handling file uploads
// const storage = multer.diskStorage({
//     destination: function (req, file, cb) {
//         cb(null, 'uploads/')
//     },
//     filename: function (req, file, cb) {
//         cb(null, file.originalname)
//     }
// });
// const upload = multer({ storage: storage });

// // Serve the HTML form
// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public/index.html'));
// });

// // Handle file data upload and initiate model training
// app.post('/upload', upload.single('dataset'), (req, res) => {
//     const model_name = req.body.modelName;
//     const dataset_path = path.join(__dirname, 'uploads', req.file.filename);
//     const target_variable = req.body.targetVariable;
//     const model_filename = `${model_name}.pkl`; // Assume model is saved as this filename

//     const execCommand = `python "${model_name}.py" "${dataset_path}" "${target_variable}"`;

//     exec(execCommand, (error, stdout, stderr) => {
//         if (error) {
//             console.error(`exec error: ${error}`);
//             return res.status(500).send(`Error training model: ${stderr}`);
//         }
//         res.send(`Model trained successfully! <a href="/download/${model_filename}">Download Model</a>`);
//     });
// });

// // Route to download the model file
// app.get('/download/:filename', (req, res) => {
//     const filename = req.params.filename;
//     const filepath = path.join(__dirname, filename);
//     if (fs.existsSync(filepath)) {
//         res.download(filepath); // Provide the file for download
//     } else {
//         res.status(404).send('File not found');
//     }
// });

// // Start the server
// app.listen(port, () => {
//     console.log(`Server is running on http://localhost:${port}`);
// });
