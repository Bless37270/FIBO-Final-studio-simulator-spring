// Wait for the Desmos calculator to load
window.addEventListener('DOMContentLoaded', () => {
  // Hide expressions list directly using JavaScript
  const expressionsList = document.querySelector('.dcg-left');
  if (expressionsList) {
      expressionsList.style.setProperty('display', 'none', 'important');
  }
  
  // Run the rest of your code after hiding expressions list
  calculator.setBlank();
  
  // Add instructions to draw the layout grid
  const minX = -10; // Minimum x-value
  const maxX = 10;  // Maximum x-value
  const minY = -10; // Minimum y-value
  const maxY = 10;  // Maximum y-value
  const step = 1;   // Step size for grid lines
  
  // Draw x-axis
  for (let i = minX; i <= maxX; i += step) {
      calculator.setExpression({ id: 'x-axis-' + i, latex: 'y=0', color: '#000000', hidden: false });
  }
  
  // Draw y-axis
  for (let i = minY; i <= maxY; i += step) {
      calculator.setExpression({ id: 'y-axis-' + i, latex: 'x=0', color: '#000000', hidden: false });
  }
  
  // Draw grid lines
  for (let i = minX + step; i < maxX; i += step) {
      calculator.setExpression({ id: 'grid-line-x-' + i, latex: 'y=0', color: '#CCCCCC', hidden: false });
  }
  for (let i = minY + step; i < maxY; i += step) {
      calculator.setExpression({ id: 'grid-line-y-' + i, latex: 'x=0', color: '#CCCCCC', hidden: false });
  }
});
