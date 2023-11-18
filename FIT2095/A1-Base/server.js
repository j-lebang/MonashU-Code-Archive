/**
 * @author Susilo Lebang <sleb0005@student.monash.edu>
 * @author Yantao He <yhee0104@student.monash.edu>
 */

const express = require("express");
const path = require("path");
const ejs = require("ejs")
const Events = require("./models/events");
const Category = require("./models/category");
const fs = require('fs');

/**
 * views path
 * @const
 */
const VIEWS_PATH = path.join(__dirname, "/views/"); 

/**
 * port number
 * @const
 */
const PORT_NUMBER = 8080;

let app = express();
let events = [];
let sold_events = [];
let category = [];

app.engine('html', ejs.renderFile);
app.set('view engine', 'html');
app.use(express.urlencoded({ extended: true }));

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

app.use('/images', express.static(path.join(__dirname, 'images')));

app.listen(PORT_NUMBER, function () {
    console.log(`listening on port ${PORT_NUMBER}`);
})

/**
 * Load the home page
 * @name get/
 */
app.get('/', function (req, res) {
    res.render("index");
});

/**
 * Send file for adding new category
 * @name get/add-category
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get("/33279500/add-category", function(req, res) {
    res.sendFile(path.join(__dirname, "views", "add-category.html"));
});

/**
 * Add new category to database and redirect to category list
 * @name post/add-category
 * @param {string} endpoint
 * @param {Function} callback
 */
app.post("/33279500/add-category", function(req, res) {
    let reqBody = req.body;

    let newCategory = new Category(reqBody.Name, reqBody.Desc, reqBody.Image);

    if (!newCategory.image.startsWith("/")) {
        newCategory.image = "/" + newCategory.image;
    }

    category.push(newCategory);
    console.log(category);
    
    res.redirect("/33279500/event-categories");
});

/**
 * Render and show all category list
 * @name get/event-categories
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get("/33279500/event-categories", function(req, res) {
    res.render(path.join(__dirname, "views", "event-categories.html"), { db: category });
});

/**
 * Search category by keyword
 * @name get/seach-category
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get("/33279500/search-category", function(req, res) {
    let keyword = String(req.query.keyword);
    keyword = keyword.toLowerCase();

    let result = [];
    for (let i = 0; i < category.length; i++) {
        let lowercase = String(category[i].desc).toLowerCase();
        if (lowercase.includes(keyword)) { result.push(category[i]); }
    }

    res.render(path.join(__dirname, "views", "event-categories.html"), { db: result });
});

/**
 * Show Event Details
 * Default page when no id is entered
 * @name get/event
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get("/33279500/event", function(req, res) {
    let temp = [{
        id: "",
        name: "",
        desc: "",
        image: "/images/unload.png",
        startDateTime: "",
        durationInMinutes: "",
        isActive: "",
        capacity: "",
        ticketsAvailable: "",
        categoryId: ""
    }];
    res.render("event.html", { db: temp, calculateEndTime: calculateEndTime });
});

/**
 * Show event details by Event ID
 * @name get/event/:id
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get("/33279500/event/:id", function(req, res) {
    let id = req.params.id;
    var temp = [];
    for (let i = 0; i < events.length; i++) {
        if (events[i].id == id) { temp.push(events[i]); break; }
    }
    res.render("event.html", { db: temp, calculateEndTime: calculateEndTime });
});

/**
 * Send file for deleting category by ID
 * @name get/delete-category
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get("/33279500/delete-category", function(req, res) {
    res.sendFile(path.join(__dirname, "views", "delete-category.html"));
});

/**
 * Delete category with given ID
 * @name post/delete-category
 * @param {string} endpoint
 * @param {Function} callback
 */
app.post("/33279500/delete-category", function(req, res) {
    let id = req.body.id;
    for (let i = 0; i < category.length; i++) {
        if (category[i].id == id) { category.splice(i, 1); break; }
    }

    res.redirect("/33279500/event-categories");
});

/**
 * Send file for adding new events
 * @name get/add-event
 * @param {string} endpoint
 * @param {Function} callback
 */
app.get('/YantaoHe/add-event', function(req, res) {
    fileName = VIEWS_PATH + "add-events.html";
    res.sendFile(fileName);
});

/**
 * Render files to show all events
 * @name get/events
 * @param {string} endpoint
 * @param {Function} callback
*/
app.get('/YantaoHe/events', function(req, res) {
    fileName = VIEWS_PATH + "events.html";
    res.render(fileName, { events: events, calculateEndTime: calculateEndTime });
});

/**
 * Render files to show all sold-out events
 * @name get/sold-out-events
 * @param {string} endpoint
 * @param {Function} callback 
*/
app.get('/YantaoHe/sold-out-events', function(req, res) {
    fileName = VIEWS_PATH + "sold-out-events.html";
    res.render(fileName, { sold_events: sold_events, calculateEndTime: calculateEndTime });
});

/**
 * Show category details
 * Default page when no id is entered
 * @name get/category
 * @param {string} endpoint
 * @param {Function} callback
*/
app.get('/YantaoHe/category', function(req, res) {
    var events = [];
    var db = [{ Id: "", Name: "", Desc: "", Image: "/unload.png", createAt: "" }];
    res.render('category.html', { calculateEndTime: calculateEndTime, events: events, db: db });
});

/**
 * Show category details by Category ID
 * @name get/category/:id
 * @param {string} endpoint
 * @param {Function} callback
*/
app.get('/YantaoHe/category/:id', function(req, res) {
    var id = req.params.id;
    var matchedEvents = events.filter(event => event.categoryId == id);
    var matchedDb = category.filter(category => category.id == id);
    if (matchedDb.length === 0) {
        matchedDb = [{ id: "", name: "", desc: "", image: "/unload.png", createAt: "" }];
    }
    res.render('category.html', { calculateEndTime: calculateEndTime, events: matchedEvents, db: matchedDb });
});

/**
 * Add new event to the database and redirect to event list
 * @name post/add-event
 * @param {string} endpoint
 * @param {Function} callback
*/
app.post('/YantaoHe/add-event/save', function(req, res) {
    let name = req.body.Name;
    let desc = req.body.Desc;
    let image = req.body.Image;
    let startDateTime = req.body.StartDateTime;
    let durationInMinutes = req.body.DurationInMinutes;
    let isActive = req.body.IsActive;
    let capacity = req.body.Capacity;
    let ticketsAvailable = req.body.TicketsAvailable;
    let categoryId = req.body.CategoryId;
    
    if (!capacity) {
        capacity = "1000";
    }
    if (!ticketsAvailable) {
        ticketsAvailable = capacity;
    }
    if (!isActive) {
        isActive = "on";
    }
    const newEvent = new Events(name, desc, image, startDateTime, durationInMinutes, isActive, capacity, ticketsAvailable, categoryId);
    
    events.push(newEvent); 
    if (ticketsAvailable === "0"){
        sold_events.push(newEvent);
    }
    
    console.log(newEvent)
    res.redirect('/YantaoHe/events');
});

/**
 * Delete an event by the event ID
 * @name get/delete-event
 * @param {string} endpoint
 * @param {Function} callback
*/
app.get('/YantaoHe/delete-event', function(req, res) {
    let eventId = req.query.eventId;
    
    let index = events.findIndex(event => event.id === eventId); // find the event with the provided id
    
    if (index > -1) {
        events.splice(index, 1); // if the event is found, remove it from the array
        
        console.log(`Event with Id = ${eventId} has been deleted`)
        res.redirect('/YantaoHe/events');
    } else {
        console.log(`No event found with Id = ${eventId}`);
        fileName = VIEWS_PATH + "delete-event.html";
        res.sendFile(fileName);
    }
});

/**
 * Function to calculate the end time
 * @function
 * @param {Date} startDateTime 
 * @param {number} durationInMinutes 
 * @returns {string}
 */
function calculateEndTime(startDateTime, durationInMinutes) {
    const startDate = new Date(startDateTime);
    const endTime = new Date(startDate.getTime() + durationInMinutes * 60000); // Convert minutes to milliseconds
    return endTime.toLocaleString(); 
}