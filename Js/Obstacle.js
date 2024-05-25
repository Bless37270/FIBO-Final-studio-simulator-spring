class Obstacle {
    constructor(calculator) {
        this.calculator = calculator;
    }

    createObstacle(x, y, width, height) {
        const expressions = [
            {
                id: 'obstacle-top',
                latex: `y=${y + height} \\{${x} \\le x \\le ${x + width}\\}`,
                color: '#FFA500'
            },
            {
                id: 'obstacle-bottom',
                latex: `y=${y} \\{${x} \\le x \\le ${x + width}\\}`,
                color: '#FFA500'
            },
            {
                id: 'obstacle-left',
                latex: `x=${x} \\{${y} \\le y \\le ${y + height}\\}`,
                color: '#FFA500'
            },
            {
                id: 'obstacle-right',
                latex: `x=${x + width} \\{${y} \\le y \\le ${y + height}\\}`,
                color: '#FFA500'
            }
        ];
        expressions.forEach(expression => this.calculator.setExpression(expression));
    }
}
