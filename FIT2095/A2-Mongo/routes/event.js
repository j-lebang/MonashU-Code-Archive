const path = require("path");
const express = require("express");
const categoryM = require("../models/category");
const eventM = require("../models/events");

const router = express.Router();
const { calculateEndTime } = require('../public/js/calcendtime')
const VIEWS_PATH = path.join(__dirname, "../views/"); 

/**
 * Send file for adding new events
 * @name get/add-event
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get('/add-event', function(req, res) {
    fileName = VIEWS_PATH + "add-events.html";
    res.sendFile(fileName);
});

/**
 * Render files to show all events
 * @name get/events
 * @param {string} endpoint
 * @param {Function} callback
*/
router.get('/events', async function(req, res) {
    fileName = VIEWS_PATH + "events.html";
    res.sendFile(fileName);
});

/**
 * Render files to show all sold-out events
 * @name get/sold-out-events
 * @param {string} endpoint
 * @param {Function} callback 
*/
router.get('/sold-out-events', async function(req, res) {
    const soldOutEvents = await eventM.Event.find({ ticketsAvailable: 0 });
    fileName = VIEWS_PATH + "sold-out-events.html";
    res.render(fileName, { sold_events: soldOutEvents, calculateEndTime: calculateEndTime });
});

/**
 * Delete an event by the event ID
 * @name get/delete-event
 * @param {string} endpoint
 * @param {Function} callback
*/
router.get('/delete-event', function(req, res) {
    fileName = VIEWS_PATH + "delete-event.html";
    res.sendFile(fileName);
});

/**
 * Show category details
 * Default page when no id is entered
 * @name get/category
 * @param {string} endpoint
 * @param {Function} callback
*/
router.get('/category', function (req, res) {
    var events = [];
    var category = { id: "", name: "", desc: "", image: "/unload.png", createAt: "" };
    res.render('category.html', {calculateEndTime: calculateEndTime, events: events, category: category});
});

/**
 * Show category details by Category ID
 * @name get/category/:id
 * @param {string} endpoint
 * @param {Function} callback
*/
router.get('/category/:id', async function (req, res) {
    let id = req.params.id;

    try {
        let category = await categoryM.Category.findOne({ id: id });
        let matchedEvents = await eventM.Event.find({ categoryList: category._id });
        res.render('category.html', { calculateEndTime: calculateEndTime, events: matchedEvents, category: category });
    } catch (error) {
        res.status(404).json({ error: error });
    }

});

module.exports = router;