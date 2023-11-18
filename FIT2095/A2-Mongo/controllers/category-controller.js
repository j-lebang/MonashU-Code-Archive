const path = require("path");

const Category = require("../models/category");
const Event = require("../models/events");

let addCategoryCounter = 0;
let deleteCategoryCounter = 0;
let updateCategoryCounter = 0;

module.exports = {
    /**
     * Add new category to database and redirect to category list
     * @name addCategory
     * @param {Function} callback
     */
    addCategory: async function(req, res) {
        let name = req.body.name;
        let desc = req.body.desc;
        let image = req.body.image;

        if (!image) { image = "/unload.png"; }

        let aCategory = new Category.Category({
            id: Category.generateCode(name),
            name: name,
            desc: desc,
            image: image
        });

        await aCategory.save();
        addCategoryCounter++;

        if (req.get("Content-Type") === "application/x-www-form-urlencoded") {
            res.redirect("/33279500/event-categories");
        } else {
            res.json({ id: aCategory.id });
        }
    },
    
    /**
     * Retrieve all existing categories
     * @name getCategories
     * @param {Function} callback 
     */
    getCategories: async function(req, res) {
        let categories = await Category.Category.find({}).populate("eventList");
        res.json(categories);
    },
    
    /**
     * Delete category with given ID
     * @name deleteCategory
     * @param {Function} callback
     */
    deleteCategory: async function(req, res) {
        let id = req.body.id;

        let theCategory = await Category.Category.findOne({ id: id });
        deleteCategoryCounter++;

        // console.log("theCategory ::\n");
        
        for (let event of theCategory.eventList) {
            // console.log("\nTHIS IS THE EVENT :: ", event);
            await Event.Event.deleteOne({ _id: event._id });
        }

        await Category.Category.deleteOne({ id: id });

        if (req.get("Content-Type") === "application/x-www-form-urlencoded") {
            res.redirect("/33279500/event-categories");
        } else {
            res.json({ acknowledged: theCategory.acknowledged, deletedCount: deleteCategoryCounter });
        }
    },
    
    /**
     * Update category with the given ID
     * @name updateCategory
     * @param {Function} callback 
     */
    updateCategory: async function(req, res) {
        let { id, name, desc } = req.body;

        let theCategory = await Category.Category.updateOne({ id: id }, { $set: { name: name, desc: desc }});
        updateCategoryCounter++;

        theCategory.matchedCount ? res.json({ status: "Update Successful" }) : res.json({ status: "Invalid ID" });
    },

    /**
     * Get the number of counts happening in each operation
     * @name getStatusCategory
     * @param {Function} callback
     */
    getStatus: async function(req, res) {
        const categoryCount = await Category.Category.countDocuments();
        res.json({ 
            categoryCount: categoryCount,
            addCategoryCounter: addCategoryCounter,
            deleteCategoryCounter: deleteCategoryCounter,
            updateCategoryCounter: updateCategoryCounter
        });
    }
}