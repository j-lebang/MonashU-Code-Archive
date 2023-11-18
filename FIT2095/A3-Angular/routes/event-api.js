const express = require("express");
const eventCont = require("../controllers/event-controller")

const router = express.Router();

router.post("/add-event",eventCont.addEvent);
router.get("/list-events",eventCont.getEvents);
router.get("/get-status",eventCont.getStatus);
router.put("/update-event",eventCont.updateEvent);
router.delete("/delete-event",eventCont.deleteById);

module.exports = router;