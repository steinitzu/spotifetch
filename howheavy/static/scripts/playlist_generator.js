// find all the tunable divs
var matches = document.querySelectorAll("div.tuneable");
console.log(matches);

// Todo: Find a way to make slider start at textbox values
Object.keys(matches).forEach(function(key) {
    var element = matches[key];
    console.log(element.id);
    var valueMin = document.getElementById('min'+element.id);
    var valueMax = document.getElementById('max'+element.id);
    var spanMin = document.getElementById('span_min'+element.id);
    var spanMax = document.getElementById('span_max'+element.id);
    console.log('max '+valueMin.value);
    console.log('min '+valueMax.value);
    slider_el = document.getElementById('slider'+element.id);
    noUiSlider.create(slider_el, {
        start: [valueMin.value, valueMax.value],
        connect: true,
        orientation: 'horizontal',
        range: {
	    'min': 0.0,
	    'max': 1.0
        },
        cssPrefix: 'noUi-'

    });


    slider_el.noUiSlider.on('update', function( values, handle ) {
	if ( handle ) {
	    valueMax.value = values[handle];
            spanMax.innerHTML = values[handle];
	} else {
	    valueMin.value = values[handle];
            spanMin.innerHTML = values[handle];
	}
    });
});
