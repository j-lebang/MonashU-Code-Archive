const express = require("express");
const path = require("path");
const ejs = require("ejs")
const fs = require('fs');
const mongoose = require('mongoose');
const { Translate } = require('@google-cloud/translate').v2;

const textToSpeech = require("@google-cloud/text-to-speech");
const client = new textToSpeech.TextToSpeechClient();

const categoryApiRouter = require("./routes/category-api");
const eventApiRouter = require("./routes/event-api");

const PORT_NUMBER = 8080;

const app = express();
const server = require("http").Server(app);
const io = require('socket.io')(server);
app.engine('html', ejs.renderFile);
app.set('view engine', 'html');

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));
app.use(express.static(path.join(__dirname,"assignment-3/dist/assignment-3")));

const translate = new Translate();

io.on('connection', (socket) => {
    console.log("We got a new socket connection",socket.id);
    socket.on('sendText', async (data) => {
        const [translation] = await translate.translate(data.text, data.language);
        socket.emit('translatedText', `${translation}`);
    });
    socket.on("text-present", async (text) => {
        const request = { 
            input: { text: text },
            voice: { languageCode: "en-AU", ssmlGender: "NEUTRAL" },
            audioConfig: { audioEncoding: "MP3" }
        }

        client.synthesizeSpeech(request, (err, response) => {
            if (err) { console.log("ERROR:", err); return; }
            fs.writeFile("output.mp3", response.audioContent, "binary", err => {
              if (err) { console.error("ERROR:", err); return; }
              console.log("Audio content written to file: output.mp3");
            });
        });
    });
});

app.use('/images', function(req, res, next) {
    const imagePath = path.join(__dirname, 'images', req.path);

    fs.access(imagePath, fs.constants.F_OK, (err) => {
        if (err) {
            res.sendFile(path.join(__dirname, 'images', 'unload.png'));
        } else {
            next();
        }
    });
});

const url = "mongodb://127.0.0.1/EMS";

async function connect(url) {
	await mongoose.connect(url);
	return "Connected Successfully";
}

app.use('/images', express.static(path.join(__dirname, 'images')));

app.use("/33279500/api/v1", categoryApiRouter);
app.use('/YantaoHe/api/v1', eventApiRouter)

connect(url)
	.then(console.log)
	.catch((err) => console.log(err));

server.listen(PORT_NUMBER, function () {
    console.log(`listening on port ${PORT_NUMBER}`);
});