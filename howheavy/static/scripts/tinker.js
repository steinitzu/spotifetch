var TrackList = React.createClass({
    render: function() {
        if (!this.props.tracks) {
            return null;
        };
        return (
            <ul className="TrackList">
            {
                this.props.tracks.map(function(track) {
                    return <li key={track.track.id}>{track.track.artist} - {track.track.name}</li>})
            }
            </ul>
            /* var rows = []
             * this.props.items.forEach(function(item) {
             *     rows.push(<li key={item.track.id}>{item.track.artist} - {item.track.name}</li>);
             * }.bind(this));
             * return (
             *     <ul>{rows}</ul>
             * );*/
        );
    }
});


define(function (require) {
    //Notice the space between require and the arguments.
    var jsonpipe = require ('/static/scripts/jsonpipe');
});


var TheTrackList = React.createClass({

    loadTracks: function() {
        var rows = [];
        jsonpipe.flow(this.props.url,
                      {'delimiter': '\r',
                       'success': function(data) {
                           console.log(data);
                           //this.setState({data:[data]});
                           rows.push(data);
                           //this.setState({data: this.state.data.concat([data])});
                       },
                       'complete': function(status_txt) {
                           this.setState({data: rows});
                       }.bind(this)
                      });

    },
    getInitialState: function() {
        return {data: []};
    },
    componentDidMount: function() {
        this.loadTracks();
        //setInterval(this.loadTracks, this.props.pollInterval);
    },
    render: function() {
        console.log('Rendering');
        //return (

        return (
            <TrackList tracks={this.state.data} />
        );
    }
});

var url = '/saved_tracks?token='
         +document.getElementById('spotify_access_token').attributes['data'].value;
ReactDOM.render(
    <TheTrackList url={url} pollInterval={10000} />,
    document.getElementById('example')
);
