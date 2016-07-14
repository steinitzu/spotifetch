/* var Track = React.createClass({
 *     render: function() {
 *         return (<li key={this.props.track.track.id}>{this.props.track.track.name}</li>);
 *     }
 * });
 *
 *
 * var TrackList = React.createClass({
 *     render: function() {
 *         var rows = []
 *         this.props.tracks.forEach(function(track) {
 *             rows.push(<Track track={track} key={track.track.id} />);
 *         }.bind(this));
 *         return (
 *             <ul>{rows}</ul>
 *         );
 *     }
 * });*/


var ItemList = React.createClass({
    render: function() {
        var rows = []
        this.props.items.forEach(function(item) {
            rows.push(<li key={item.number}>{item.number}</li>);
        }.bind(this));
        return (
            <ul>{rows}</ul>
        );
    }

});


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


var url = '/saved_tracks?token='
         +document.getElementById('spotify_access_token').attributes['data'].value;

define(function (require) {
    //Notice the space between require and the arguments.
    var jsonpipe = require ('/static/scripts/jsonpipe');
});

var track_rows = []


var TheTrackList = React.createClass({
    loadTracks: function() {
    }
});


jsonpipe.flow(url,
              {'delimiter': '\r',
               'success': function(data) {
                   track_rows.push(data);
                   ReactDOM.render(
                       <TrackList tracks={track_rows} />,
                       document.getElementById('example')
                   );
                   /* ReactDOM.render(
                    *     <div><p>Loading data</p></div>,
                    *     document.getElementById('example')
                    * );*/
               },
               'complete': function(statusText) {

               }
              })

console.log('shitfck');






/* TODO: https://jakearchibald.com/2015/thats-so-fetch/ check partialcells stuff */
/* fetch(url).then(response => {
 *     var decoder = new TextDecoder();
 *     var reader = response.body.getReader();
 *     var items = [];
 *
 *     reader.read().then(function processResult(result) {
 *         if (result.done) {
 *             console.log('Fetch complete');
 *             return;
 *         }
 *         var result_data = decoder.decode(result.value, {stream: true});
 *
 *         console.log(result_data);
 *         var result_data = '[' + result_data.substring(0, result_data.length - 1) + ']'
 *         items.push(JSON.parse(result_data)[0]);
 *         ReactDOM.render(
 *             <TrackList items={items} />,
 *             document.getElementById('example')
 *         );
 *
 *         return reader.read().then(processResult);
 *     });
 * });*/





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
