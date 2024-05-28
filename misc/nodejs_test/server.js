// https://www.w3schools.com/nodejs/nodejs_raspberrypi.asp
// https://medium.com/@imajeet5/how-to-serve-files-using-node-js-d99de4653a3
// to run type in terminal "npm install express" (first time only)
// then "node server.js"

const express = require('express');
const path = require('path');
//const fs = require('fs');

const app = express();

//serve static files 
app.use(express.static(path.join(__dirname, 'public')));

//download the file when the button is clicked
app.get('/download-file', (req, res) => {
    const filePath = path.join(__dirname, "./files/serialize_test.pkl");
    res.download(filePath, "serialize_test.pkl");
});

//listen for requests
app.listen(3000, () => {
  console.log(`Server is running on http://localhost:${3000}`);
});

