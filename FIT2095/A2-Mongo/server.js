/**
 * @author Susilo Lebang <sleb0005@student.monash.edu>
 * @author Yantao He <yhee0104@student.monash.edu>
 */

const express = require("express");
const path = require("path");
const ejs = require("ejs")
const fs = require('fs');
const mongoose = require('mongoose');

const categoryRouter = require("./routes/category");
const categoryApiRouter = require("./routes/category-api");
const eventRouter = require("./routes/event");
const eventApiRouter = require("./routes/event-api");


/**
 * Port number
 * @const
 */
const PORT_NUMBER = 8080;

const app = express();

app.engine('html', ejs.renderFile);
app.set('view engine', 'html');

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));

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

/**
 * URL for mongodb
 * @const
 */
const url = "mongodb://127.0.0.1/EMS";

/**
 * Function to connect to mongodb
 * @name connecttomongo
 * @param {String} url 
 * @returns {String}
 */
async function connect(url) {
	await mongoose.connect(url);
	return "Connected Successfully";
}

app.use('/images', express.static(path.join(__dirname, 'images')));

/**
 * To use the normal category router
 * @name use/33279500
 * @param {String} endpoint
 * @param {Function} callback
 */
app.use("/33279500", categoryRouter);

/**
 * To use the api category router
 * @name use/33279500/api/v1
 * @param {String} endpoint
 * @param {Function} callback
 */
app.use("/33279500/api/v1", categoryApiRouter);

/**
 * To use the normal event router
 * @name use/YantaoHe
 * @param {String} endpoint
 * @param {Function} callback
 */
app.use('/YantaoHe', eventRouter)

/**
 * To use the api event router
 * @name use/YantaoHe/api/v1
 * @param {String} endpoint
 * @param {Function} callback
 */
app.use('/YantaoHe/api/v1', eventApiRouter)

/**
 * Load the home page
 * @name get/
 * @param {String} endpoint
 * @param {Function} callback
 */
app.get("/", function(req, res) {
    res.sendFile(path.join(__dirname, "views", "index.html"));
});

/**
 * Wait for connection from mongodb
 * @name connect
 * @param {String}
 */
connect(url)
	.then(console.log)
	.catch((err) => console.log(err));

app.listen(PORT_NUMBER, function () {
    console.log(`listening on port ${PORT_NUMBER}`);
})