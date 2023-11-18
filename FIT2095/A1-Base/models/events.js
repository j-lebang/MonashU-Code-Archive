function generateCode() {
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
class Events {
    constructor(name, desc, image, startDateTime, durationInMinutes, isActive, capacity, ticketsAvailable, categoryId) {
        var code=generateCode();
        this.id = code;
        this.name = name;
        this.desc = desc;
        this.image = image;
        this.startDateTime = startDateTime;
        this.durationInMinutes = durationInMinutes;
        this.isActive = isActive;
        this.capacity = capacity;
        this.ticketsAvailable = ticketsAvailable;
        this.categoryId = categoryId;
    }
}
module.exports=Events;