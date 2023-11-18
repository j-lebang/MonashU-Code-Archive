const express = require("express");

const categoryCont = require("../controllers/category-controller");

const router = express.Router();

router.post("/add-category", categoryCont.addCategory);
router.get("/event-categories", categoryCont.getCategories);
router.delete("/delete-category", categoryCont.deleteCategory);
router.put("/update-category", categoryCont.updateCategory);
router.get("/get-status", categoryCont.getStatus);

module.exports = router;