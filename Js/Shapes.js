class Shapes {
    constructor(calculator) {
        this.calculator = calculator;
    }

    createShapes(x, y, width, height) {
        const expressions = [
            {
                id: 'shape-top',
                latex: `y=${y + height} \\{${x} \\le x \\le ${x + width}\\}`,
                color: '#0000FF'
            },
            {
                id: 'shape-bottom',
                latex: `y=${y} \\{${x} \\le x \\le ${x + width}\\}`,
                color: '#0000FF'
            },
            {
                id: 'shape-left',
                latex: `x=${x} \\{${y} \\le y \\le ${y + height}\\}`,
                color: '#0000FF'
            },
            {
                id: 'shape-right',
                latex: `x=${x + width} \\{${y} \\le y \\le ${y + height}\\}`,
                color: '#0000FF'
            }
        ];
        expressions.forEach(expression => this.calculator.setExpression(expression));
    }
}
