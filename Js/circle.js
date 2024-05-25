class Circle {
    constructor(radius, x, y) {
        this.radius = radius;  // Radius of the circle
        this.x = x;            // X-coordinate of the center
        this.y = y;            // Y-coordinate of the center
    }

    // Method to calculate the area of the circle
    getArea() {
        return Math.PI * this.radius * this.radius;
    }

    // Method to calculate the circumference of the circle
    getCircumference() {
        return 2 * Math.PI * this.radius;
    }

    // Method to describe the circle
    describe() {
        return `Circle with radius ${this.radius} at point (${this.x},${this.y})`;
    }
}

// Example of creating a circle instance
let myCircle = new Circle(0.5, 0, 0.5);
console.log(myCircle.describe());
console.log("Area:", myCircle.getArea());
console.log("Circumference:", myCircle.getCircumference());
