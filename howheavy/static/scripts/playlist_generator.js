// find all the tunable divs
var matches = document.querySelectorAll("div.tuneable");
console.log(matches);


Object.keys(matches).forEach(function(key) {
    var element = matches[key];
    console.log(element.id);
    slider_el = document.getElementById('slider'+element.id);
    noUiSlider.create(slider_el, {
        start: [0.0, 1.0],
        connect: true,
        orientation: 'horizontal',
        range: {
	    'min': 0.0,
	    'max': 1.0
        },
        cssPrefix: 'noUi-'

    });

    var valueMin = document.getElementById('min'+element.id);
    var valueMax = document.getElementById('max'+element.id);
    var spanMin = document.getElementById('span_min'+element.id);
    var spanMax = document.getElementById('span_max'+element.id);
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
