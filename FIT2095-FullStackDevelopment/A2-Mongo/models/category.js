const path = require("path");
const mongoose = require("mongoose");

const categorySchema = mongoose.Schema({
    id: {
        type: String,
        required: true
    },
    name: {
        type: String,
        validate: { 
            validator: function(_name) { 
                for (char of _name) {
                    if (('a' <= char && char <= 'z') ||
                        ('A' <= char && char <= 'Z') ||
                        ('0' <= char && char <= '9')) continue;
                    return false;
                }
            },
            message: "Please enter alphanumeric values"
        },
        required: true
    },
    desc: {
        type: String,
        default: ""
    },
    image: {
        type: String,
    },
    eventList: [
        {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Event"
        }
    ],
    createdAt: {
        type: Date,
        default: new Date()
    }
});

module.exports = {
    Category: mongoose.model("Category", categorySchema),

    generateCode: function(_name) {
        const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        let code = Math.round(Math.random() * 10000);
        while (code < 1000) code *= 10;
        code = code.toString();
        code = '-' + code;

        for (let i = 0; i < 2; i++) {
            const randomIndex = Math.floor(Math.random() * characters.length);
            code = characters[randomIndex] + code;
        }
        code = 'C' + code;
    
        return code;
    }
}