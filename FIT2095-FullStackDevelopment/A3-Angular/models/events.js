/**
 * @constructor
 * @param {string} name - Name of the event
 * @param {string} desc - Description of the event
 * @param {string} image - Path to the image of the event
 * @param {Date} startDateTime - Start date of the event
 * @param {number} durationInMinutes - Duration of the event in minutes
 * @param {boolean} isActive - Indicator whether the event is currently active
 * @param {number} capacity - Capacity of the event
 * @param {number} ticketsAvailable - Tickets available for the event
 * @param {string} categoryId - The category ID in which this event belongs to
 */


const mongoose = require("mongoose");

const eventSchema = mongoose.Schema({
    id: {
        type: String,
        required: true,
    },
    name: {
        type: String,
        required: true,
    },
    desc: {
        type: String,
    },
    image: {
        type: String,
    },
    startDateTime: {
        type: String,
        required: true,
    },
    durationInMinutes: {
        type: Number,
        required: true,
    },
    isActive: {
        type: String,
        required: true,
    },
    capacity: {
        type: Number,
        validate: {
            validator: function(value) {
                return true; 
            },
        },
        default: 1000, 
    },
    ticketsAvailable: {
        type: String,
        validate: {
            validator: function(value) {
                return true; 
            },
        },
        default: function () {
            return this.capacity || 1000;
        },
    },
    categoryList: {
        type: [{type: mongoose.Schema.Types.ObjectId, ref: "Category"}]
    }
});

module.exports = {
    Event: mongoose.model("Event", eventSchema),
    generateCode: function() {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let code = 'E';
    
        // Generate two random uppercase letters
        for (let i = 0; i < 2; i++) {
            const randomIndex = Math.floor(Math.random() * characters.length);
            code += characters.charAt(randomIndex);
        }
    
        // Add a hyphen
        code += '-';
    
        // Generate four random digits 
        code += Math.round(Math.random() * 10000);
        
        return code;
    }
};