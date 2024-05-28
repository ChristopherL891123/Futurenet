// very helpful book: https://www.packtpub.com/en-us/product/nodejs-design-patterns-9781839214110?type=print&gad_source=1
// node js crash courses: https://www.youtube.com/watch?v=fUJ3ULyyA-Y 
// https://www.youtube.com/watch?v=gyQyk80_upM

const express = require("express");
const multer = require("multer");
const path = require("path");
const { exec } = require("child_process");
const fs = require("fs");

const app = express();
const port = 3000;

// handle json server features
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// handle file upload features
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, path.join(__dirname, "uploads")),
    filename: (req, file, cb) => cb(null, file.originalname)
});
const upload = multer({ storage: storage });

// globally store username
let currentUser = null;

app.get('/', (req, res) => res.sendFile(path.join(__dirname, "public", "index.html")));

// login endpoint
app.post("/login", (req, res) => {
    const usersFile = path.join(__dirname, "users.json");
    let users = {};

    if (fs.existsSync(usersFile)) {
        users = JSON.parse(fs.readFileSync(usersFile, "utf8"));
    }

    const { username, password } = req.body;
    if (users[username] && users[username].password === password) {
        currentUser = { username, role: users[username].role }; 
        res.json({ message: "Login successful", user: currentUser });
    } else {
        res.status(401).json({ message: "Invalid username or password" });
    }
});

// account registration endpoint
app.post("/register", (req, res) => {
    const usersFile = path.join(__dirname, "users.json");
    let users = {};

    if (fs.existsSync(usersFile)) {
        users = JSON.parse(fs.readFileSync(usersFile, "utf8"));
    }

    const { username, password, role } = req.body;
    if (users[username]) {
        return res.status(409).json({ message: "Username already exists" });
    }

    users[username] = { password, role };
    fs.writeFileSync(usersFile, JSON.stringify(users, null, 2));
    res.status(201).json({ message: "User registered successfully" });
});

app.post("/upload", upload.single("dataset"), async (req, res) => {
    if (!currentUser) {
        return res.status(403).send("No user logged in.");
    }

    const username = currentUser.username;
    const modelRecordPath = path.join(__dirname, "models", "model_record.json");

    let allUserModelRecords = {};
    if (fs.existsSync(modelRecordPath)) {
        allUserModelRecords = JSON.parse(fs.readFileSync(modelRecordPath, "utf8"));
    }

    let userModelRecord = allUserModelRecords[username];
    if (!userModelRecord) {
        userModelRecord = {
            "BayesianRegression": 0,
            "GradientBoostRegression": 0,
            "KMeans": 0,
            "KModes": 0,
            "KNeighbors": 0,
            "NaiveBayesClassifier": 0,
            "RandomForestClassifier": 0,
            "SpectralClustering": 0,
            "xgbClassifier": 0
        };
        allUserModelRecords[username] = userModelRecord; 
    }
    fs.writeFileSync(modelRecordPath, JSON.stringify(allUserModelRecords, null, 2));


    const { modelName: model_name, targetVariable: target_variable, clusterNumber: clusterNumber } = req.body;
    
    const dataset_path = path.join(__dirname, "uploads", req.file.filename);
    const model_identifier = userModelRecord[model_name] || 0;
    const model_filename = `${model_name}_${model_identifier}.pkl`;
    const model_graph = `${model_name}_${model_identifier}.png`;
    const script_path = path.join(__dirname, "models", "src", `${model_name}.py`);
    const defaultPath = "C:\\Users\\124ch\\Desktop\\CAPSTONE\\s24-capstone-project-ChristopherL891123";


    exec(`python "${script_path}" "${dataset_path}" "${target_variable}" "${username}" "${clusterNumber}" "${defaultPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(`Error training model: ${stderr}`);
        }

        userModelRecord[model_name] = model_identifier + 1;

        fs.writeFileSync(modelRecordPath, JSON.stringify(allUserModelRecords, null, 2));
        res.send(`Model trained successfully! <a href="/download/${model_filename}">Download Model</a> <br> Graph generated successfully! <a href="/download/${model_graph}">Download Graph</a>`);
        res.send();
    });
});


app.get("/download_graph/:filename", (req, res) => {
    const filepath = path.join(__dirname, req.params.filename);
    res.download(filepath, err => {
        if (err) {
            console.error(`Error downloading file: ${req.params.filename}`, err);
            res.status(404).send("File not found or error in downloading");
        }
    });
});

app.get("/download/:filename", (req, res) => {
    const filepath = path.join(__dirname, "models", req.params.filename);
    res.download(filepath, err => {
        if (err) {
            console.error(`Error downloading file: ${req.params.filename}`, err);
            res.status(404).send("File not found or error in downloading");
        }
    });
});

app.get("/download-logs", async (req, res) => {
    const downloadsLogPath = path.join(__dirname, "downloadsLog.json");
    try {
        const data = fs.existsSync(downloadsLogPath) ? await fs.promises.readFile(downloadsLogPath, "utf8") : '{}';
        const username = currentUser ? currentUser.username : null; 
        res.json({ user: { username }, logs: JSON.parse(data) }); 
    } catch (err) {
        console.error("Error reading the download logs:", err);
        res.status(500).send("Failed to read logs");
    }
});

app.get("/download-trial", (req, res) => {
    const trialText = "This is a trial download to confirm your connection.";
    const trialFilename = "trial_download.txt";

    const tempFilePath = path.join(__dirname, trialFilename);
    fs.writeFile(tempFilePath, trialText, err => {
        if (err) {
            console.error("Error creating trial download:", err);
            return res.status(500).send("Failed to create trial download");
        }
        res.download(tempFilePath, trialFilename, err => {
            if (err) {
                console.error("Error downloading trial file:", err);
                res.status(500).send("Failed to download trial file");
            }
            fs.unlink(tempFilePath, err => {
                if (err) {
                    console.error("Error deleting trial file:", err);
                }
            });
        });
    });
});

app.post("/generate-elbow-graph", upload.single("dataset"), (req, res) => {
    if (!currentUser) {
        return res.status(403).send("No user logged in.");
    }

    const { modelName } = req.body;
    const datasetPath = path.join(__dirname, "uploads", req.file.filename);
    const scriptPath = path.join(__dirname, "models", "src", "elbow_graph.py");
    const defaultPath = "C:\\Users\\124ch\\Desktop\\CAPSTONE\\s24-capstone-project-ChristopherL891123";

    console.log("______________________________________________________________");
    console.log(currentUser);
    console.log("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
    exec(`python "${scriptPath}" "${datasetPath}" "${modelName}" "${currentUser}" "${defaultPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(`Error generating elbow graph: ${stderr}`);
        }
        res.send(`Elbow graph generated successfully! Output: ${stdout}`);
    });
});


app.get("/download-elbow-graph/:model", (req, res) => {
    const model = req.params.model;
    const username = currentUser.username; 
    const filepath = path.join(__dirname, "models", "src", `${model}_elbow.png`);

    if (fs.existsSync(filepath)) {
        res.download(filepath, err => {
            if (err) {
                console.error(`Error downloading file: ${model}_elbow.png`, err);
                res.status(404).send("File not found or error in downloading");
            }
        });
    } else {
        res.status(404).send("File not found.");
    }
});



app.listen(port, () => console.log(`Server is running on http://localhost:${port}`));


