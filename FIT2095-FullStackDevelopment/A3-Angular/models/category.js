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
                if (_name.length < 2) return false;
                for (char of _name) {
                    if (('a' <= char && char <= 'z') ||
                        ('A' <= char && char <= 'Z') ||
                        ('0' <= char && char <= '9')) continue;
                    return false;
                }
                return true;
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
        default: path.join(__dirname, "../images", "unload.png")
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
        let code = Math.round(Math.random() * 10000);
        while (code < 1000) code *= 10;
        code = 'C' + _name[0].toUpperCase() + _name[1].toUpperCase() + '-' + code.toString();
        return code;
    }
}