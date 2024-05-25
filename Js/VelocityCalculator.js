class VelocityCalculator {
    constructor(mass, spring, displacement) {
        this.mass = mass;
        this.spring = spring;
        this.displacement = displacement;
    }

    calculateVelocity() {
        if (this.mass <= 0) {
            throw new Error("Mass must be greater than zero.");
        }
        return Math.sqrt((this.spring * Math.pow(this.displacement, 2)) / this.mass);
    }
}