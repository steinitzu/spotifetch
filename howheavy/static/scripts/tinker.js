var Track = React.createClass({
    render: function() {
        return (<li key={this.props.track.track.id}>{this.props.track.track.name}</li>);
    }
});


var TrackList = React.createClass({
    render: function() {
        var rows = []
        this.props.tracks.forEach(function(track) {
            rows.push(<Track track={track} key={track.track.id} />);
        }.bind(this));
        return (
            <ul>{rows}</ul>
        );
    }
});


var url = '/saved_tracks?token='
         +document.getElementById('spotify_access_token').attributes['data'].value;

fetch(url).then(response => {
    var decoder = new TextDecoder();
    var reader = response.body.getReader();
    reader.read().then(function processResult(result) {
        if (result.done) {
            console.log('Fetch complete');
            return;
        }
        console.log(
            decoder.decode(result.value, {stream: true})
        );
        return reader.read().then(processResult);
    });
});


/* fetch('/saved_tracks?token='
 *      +document.getElementById('spotify_access_token').attributes['data'].value)
 *     .then(function(response) {
 *         var reader = response.body.getReader();
 *         var decoder = new TextDecoder();
 *         reader.read().then(function processResult(result) {
 *             if (result.done) return;
 *             console.log(decoder.decode(result.value, {stream: true}));
 *         });
 *         return reader.read().then(processResult());
 *     })*/

        /*
         * return response.json()
           }).then(function(json) {
         * json.forEach(function(track) {
         *     console.log(track.track.name);
         * });
           });*/





/* fetch('/saved_tracks?token='
 *      +document.getElementById('spotify_access_token').attributes['data'].value)
 *     .then(function(response) {
 *         return response.json()
 *     }).then(function(json) {
 *         ReactDOM.render(
 *             <TrackList tracks={json} />,
 *             document.getElementById('example')
 *         );
 *     })*/
