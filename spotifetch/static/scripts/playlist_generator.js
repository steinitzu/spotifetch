// find all the tunable divs
var matches = document.querySelectorAll("div.tuneable");
console.log(matches);

Object.keys(matches).forEach(function(key) {
    var element = matches[key];
    console.log(element.id);
    var valueMin = document.getElementById('min'+element.id);
    var valueMax = document.getElementById('max'+element.id);
    var spanMin = document.getElementById('span_min'+element.id);
    var spanMax = document.getElementById('span_max'+element.id);
    console.log('min '+valueMin.value);
    console.log('max '+valueMax.value);
    console.log('min cap '+valueMin.getAttribute('default'));
    console.log('max cap '+valueMax.getAttribute('default'));
    slider_el = document.getElementById('slider'+element.id);
    noUiSlider.create(slider_el, {
        start: [valueMin.value, valueMax.value],
        connect: true,
        orientation: 'horizontal',
        step: parseFloat(valueMin.getAttribute('step')),
        range: {
	    'min': parseFloat(valueMin.getAttribute('default')),
	    'max': parseFloat(valueMax.getAttribute('default'))
        },
        cssPrefix: 'noUi-'

    });

    slider_el.noUiSlider.on('update', function( values, handle ) {
        field_type = valueMax.getAttribute('field_type');
        if (field_type === 'IntegerField') {
            val = parseInt(values[handle]);
        }
        else {
            val = values[handle];
        };
	if ( handle ) {
	    valueMax.value = val;
            spanMax.innerHTML = val;
	} else {
	    valueMin.value = val;
            spanMin.innerHTML = val;
	}
    });
});
