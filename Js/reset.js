function resetInputFields() {
    var coordinateOfTarget2 = document.querySelector('.coordinate-of-target2');
    var coordinateOfTarget3 = document.querySelector('.coordinate-of-target3');
    var coordinateOfTargetx = document.querySelector('.coordinate-of-targetx');
    var coordinateOfTargety = document.querySelector('.coordinate-of-targety');
    var coordinateOfTargetz = document.querySelector('.coordinate-of-targetz');

    if (coordinateOfTarget2) coordinateOfTarget2.textContent = '';
    if (coordinateOfTarget3) coordinateOfTarget3.textContent = '';
    if (coordinateOfTargetx) coordinateOfTargetx.textContent = '';
    if (coordinateOfTargety) coordinateOfTargety.textContent = '';
    if (coordinateOfTargetz) coordinateOfTargetz.textContent = '';
}