const eventM = require("../models/events");
const categoryM = require("../models/category");
const path = require("path");
const VIEWS_PATH = path.join(__dirname, "../views/");

let addEventCount = 0;
let updateEventCount = 0;
let deleteEventCount = 0;
module.exports = {
    /**
     * Add new event to the database and redirect to event list
     * @name addEvent
     * @param {Function} callback 
     */
    addEvent: async function(req, res) {
        let name = req.body.name;
        let desc = req.body.description;
        let image = req.body.image || null;
        let startDateTime = req.body.startDateTime;
        let durationInMinutes = req.body.durationInMinutes;
        let isActive = req.body.isActive || "on";
        let capacity = req.body.capacity || 1000;
        let ticketsAvailable = req.body.ticketsAvailable || capacity;
        let categories = req.body.categories;
        const categoryList = categories.split(",");
        const newEvent = new eventM.Event({
            id: eventM.generateCode(),
            name: name,
            desc: desc,
            image: image,
            startDateTime: startDateTime,
            durationInMinutes: durationInMinutes,
            isActive: isActive,
            capacity: capacity,
            ticketsAvailable: ticketsAvailable
        });
        
        try {
            for (const category of categoryList) {
                const c = await categoryM.Category.findOne({ id: category });
        
                if (c !== null) {
                    newEvent.categoryList.push(c._id);
                    c.eventList.push(newEvent._id);
                    await c.save();
                } else {
                    const newCategory = new categoryM.Category({
                        id: categoryM.generateCode(category),
                        name: category,
                        desc: "",
                        image: "",
                        createdAt: new Date()
                    });
        
                    await newCategory.validate();
                    const savedCategory = await newCategory.save();
                    console.log(savedCategory);
                    newEvent.categoryList.push(savedCategory._id);
                }
            }
        
            await newEvent.validate();
            const savedEvent = await newEvent.save();
            console.log(savedEvent);
            addEventCount++;
            
        
            if (req.get('Content-Type') === 'application/x-www-form-urlencoded') {
                res.redirect('/YantaoHe/events');
            } else {
                res.json({ eventId: savedEvent.id });
            }
        } catch (err) {
            console.error(err);
            res.status(500).json({ error: err.message });
        }
    },

    /**
     * Retrieve all existing events
     * @name getEvents
     * @param {Function} callback 
     */
    getEvents: async function(req, res) {
        const { eventId } = req.query;
        const matchedEvents = await eventM.Event.find(eventId ? {id: eventId} : {}).populate("categoryList");
        res.status(200).json(matchedEvents);
        
    },

    /**
     * Delete event with given ID
     * @name deleteById
     * @param {Function} callback 
     */
    deleteById: async function(req, res) {
        const { eventId } = req.body;
		let obj = await eventM.Event.deleteOne({ id: eventId });
        deleteEventCount++;
		res.json(obj);
    },

    /**
     * Update event with the given ID
     * @name updateEvent
     * @param {Function} callback
     */
    updateEvent: async function(req, res) {
        const { eventId, name, capacity } = req.body;

        const result = await eventM.Event.updateOne({ id:eventId }, { name, capacity });

        if (result.matchedCount > 0) {
            updateEventCount++
            res.json({ status: 'updated successfully' });
        } else {
            res.status(404).json({ status: 'ID not found' });
        }
    },

    /**
     * @name getStatusEvent
     * @param {Function} callback 
     */
    getStatus: async function(req, res) {
        const eventCount = await eventM.Event.countDocuments();
        res.json({ eventCount: eventCount ,addEventCount: addEventCount, updateEventCount: updateEventCount, deleteEventCount: deleteEventCount});
    },
};