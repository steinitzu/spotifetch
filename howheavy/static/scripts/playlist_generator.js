// var make_slider = function(field) {
//     var slider = document.getElementById('slider');
// }

// noUiSlider.create(slider, {
//     start: [0.0, 1.0],
//     connect: true,
//     range: {
// 	'min': 0.0,
// 	'max': 1.0
//     }
// });


// var valueMin = document.getElementById('min_acousticness');
// var valueMax = document.getElementById('max_acousticness');

// // When the slider value changes, update the input and span
// slider.noUiSlider.on('update', function( values, handle ) {
// 	if ( handle ) {
// 		valueMax.value = values[handle];
// 	} else {
// 		valueMin.value = values[handle];
// 	}
// });

// find all the tunable divs
var matches = document.querySelectorAll("div.tuneable");
console.log(matches);


Object.keys(matches).forEach(function(key) {
    var element = matches[key];
//matches.forEach(function(element) {
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
            //valueMax.setAttribute('value', values[handle]);
	} else {
	    valueMin.value = values[handle];
            spanMin.innerHTML = values[handle];
            //valueMin.setAttribute('value', values[handle]);
	}
    });
});




// When the slider value changes, update the input and span





// When the input changes, set the slider value
// valueMax.addEventListener('change', function(){
// 	slider.noUiSlider.set([null, this.value]);
// });

// valueMin.addEventListener('change', function(){
// 	slider.noUiSlider.set([null, this.value]);
// });
