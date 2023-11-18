/**
 * Function to calculate the end time
 * @name calculateEndTime
 * @param {*} startDateTime 
 * @param {*} durationInMinutes 
 * @returns {string}
 */
function calculateEndTime(startDateTime, durationInMinutes) {
    const startDate = new Date(startDateTime);
    const endTime = new Date(startDate.getTime() + durationInMinutes * 60000); // Convert minutes to milliseconds
    return endTime.toLocaleString(); 
}

module.exports = { calculateEndTime };