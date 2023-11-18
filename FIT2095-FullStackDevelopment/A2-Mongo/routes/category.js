const express = require("express");
const path = require("path");

const Category = require("../models/category");
const CategoryCont = require("../controllers/category-controller");
const Event = require("../models/events");
const { calculateEndTime } = require("../public/js/calcendtime");

const router = express.Router();

/**
 * Send file for adding new category
 * @name get/add-category
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get("/add-category", function(req, res) {
    res.sendFile(path.join(__dirname, "../views", "add-category.html"));
});

/**
 * Render and show all category list
 * @name get/event-categories
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get("/event-categories", async function(req, res) {
    let category = await Category.Category.find({});
    res.render(path.join(__dirname, "../views", "event-categories.html"), { db: category });
});

/**
 * Search category by keyword
 * @name get/seach-category
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get("/search-category", async function(req, res) {
    let keyword = String(req.query.keyword);
    keyword = keyword.toLowerCase();

    let category = await Category.Category.find({});

    let result = [];
    for (let i = 0; i < category.length; i++) {
        let lowercase = String(category[i].desc).toLowerCase();
        if (lowercase.includes(keyword)) { result.push(category[i]); }
    }

    res.render(path.join(__dirname, "../views", "event-categories.html"), { db: result });
});

/**
 * Send file for deleting category by ID
 * @name get/delete-category
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get("/delete-category", function(req, res) {
    res.sendFile(path.join(__dirname, "../views", "delete-category.html"));
});

/**
 * Show Event Details
 * Default page when no id is entered
 * @name get/event
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get("/event", function(req, res) {
    let temp = [{
        id: "",
        name: "",
        desc: "",
        image: path.join(__dirname, "../images", "unload.png"),
        startDateTime: "",
        durationInMinutes: "",
        isActive: "",
        capacity: "",
        ticketsAvailable: "",
        categoryId: ""
    }];

    res.render(path.join(__dirname, "../views", "event.html"), { db: temp, calculateEndTime: calculateEndTime });
});

/**
 * Show event details by Event ID
 * @name get/event/:id
 * @param {string} endpoint
 * @param {Function} callback
 */
router.get("/event/:id", async function(req, res) {
    let id = req.params.id;
    let event = await Event.Event.find({ id: id });

    res.render(path.join(__dirname, "../views", "event.html"), { db: event, calculateEndTime: calculateEndTime });
});

module.exports = router;