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

fetch('/saved_tracks?token='
     +document.getElementById('spotify_access_token').attributes['data'].value)
    .then(function(response) {
        return response.json()
    }).then(function(json) {
        ReactDOM.render(
            <TrackList tracks={json} />,
            document.getElementById('example')
        );
    })
