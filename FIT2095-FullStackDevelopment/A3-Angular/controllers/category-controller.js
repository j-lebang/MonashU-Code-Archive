const path = require("path");

const Category = require("../models/category");
const Event = require("../models/events");

let addCategoryCounter = 0;
let deleteCategoryCounter = 0;
let updateCategoryCounter = 0;

module.exports = {
    addCategory: async function(req, res) {
        let name = req.body.name;
        let desc = req.body.desc;
        let image = req.body.image;

        try {
            let aCategory = new Category.Category({
                id: Category.generateCode(name),
                name: name,
                desc: desc,
                image: image
            });
    
            await aCategory.save();
            addCategoryCounter++;

            res.json({ id: aCategory.id });
        } catch (error) {
            res.status(400).json({ error: error });
        }
    },
    
    getCategories: async function(req, res) {
        const { id } = req.query;
        let categories = await Category.Category.find(id ? { id: id } : {}).populate("eventList");
        res.json(categories);
    },
    
    deleteCategory: async function(req, res) {
        let id = req.body.id;

        let theCategory = await Category.Category.findOne({ id: id });
        deleteCategoryCounter++;

        for (let event of theCategory.eventList) {
            await Event.Event.deleteOne({ _id: event._id });
        }

        await Category.Category.deleteOne({ id: id });

        if (req.get("Content-Type") === "application/x-www-form-urlencoded") {
            res.redirect("/33279500/event-categories");
        } else {
            res.json({ acknowledged: theCategory.acknowledged, deletedCount: deleteCategoryCounter });
        }
    },
    
    updateCategory: async function(req, res) {
        let { id, name, desc } = req.body;

        let theCategory = await Category.Category.updateOne({ id: id }, { $set: { name: name, desc: desc }});
        updateCategoryCounter++;

        theCategory.matchedCount ? res.json({ status: "Update Successful" }) : res.json({ status: "Invalid ID" });
    },

    getStatus: async function(req, res) {
        const categoryCount = await Category.Category.countDocuments();
        const eventCount = await Event.Event.countDocuments();
        res.json({ 
            categoryCount: categoryCount,
            eventCount: eventCount
        });
    }
}