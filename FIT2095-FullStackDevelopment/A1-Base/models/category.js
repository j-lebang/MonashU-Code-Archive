/**
 * @constructor
 * @param {string} name - Name of the category
 * @param {string} desc - Description of the category
 * @param {string} image - Path to the image of the category
 */
class Category {
    constructor(name, desc, image) {
        this.id = Math.round(Math.random() * 10000);
        while (this.id < 1000) this.id *= 10;

        this.name = name;
        this.desc = desc;
        this.image = image;
        
        this.id = 'C' + this.name[0].toUpperCase() + this.name[1].toUpperCase() + '-' + this.id.toString();

        this.createdAt = new Date();
        this.createdAt = `${ this.createdAt.getDate() }/${ this.createdAt.getMonth() + 1 }/${ this.createdAt.getFullYear() }`
    }
}

module.exports = Category;