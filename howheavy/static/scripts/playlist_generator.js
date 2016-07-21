var make_slider = function(field) {
    var slider = document.getElementById('slider');
}

noUiSlider.create(slider, {
    start: [0.0, 1.0],
    connect: true,
    range: {
	'min': 0.0,
	'max': 1.0
    }
});


var valueMin = document.getElementById('min_acousticness');
var valueMax = document.getElementById('max_acousticness');

// When the slider value changes, update the input and span
slider.noUiSlider.on('update', function( values, handle ) {
	if ( handle ) {
		valueMax.value = values[handle];
	} else {
		valueMin.value = values[handle];
	}
});

// find all the tunable divs
var matches = document.querySelectorAll("div.tuneable");
console.log(matches);

// When the input changes, set the slider value
// valueMax.addEventListener('change', function(){
// 	slider.noUiSlider.set([null, this.value]);
// });

// valueMin.addEventListener('change', function(){
// 	slider.noUiSlider.set([null, this.value]);
// });
