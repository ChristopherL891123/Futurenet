const express = require('express');
const multer  = require('multer');
const path = require('path');

const app = express();
const port = 3000;

// Multer setup to handle file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/') // save uploads in 'uploads/' directory
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname) // keep original file name
    }
});

const upload = multer({ storage: storage });

// Serve the HTML form
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/index.html'));
});

// Handle file upload
app.post('/upload', upload.single('file'), (req, res) => {
    res.send('File uploaded successfully!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
