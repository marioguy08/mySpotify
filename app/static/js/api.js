var apiUrl = 'http://localhost:8080';

// PRIVATE METHODS

/**
 * HTTP GET request 
 * @param  {string}   url       URL path, e.g. "/api/playlists/<id>"
 * @param  {function} onSuccess   callback method to execute upon request success (200 status)
 * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
 * @return {None}
 */
var makeGetRequest = function (url, onSuccess, onFailure) {
    $.ajax({
        type: 'GET',
        url: apiUrl + url,
        dataType: "json",
        success: onSuccess,
        error: onFailure
    });
};

/**
 * HTTP POST request
 * @param  {string}   url       URL path, e.g. "/api/playlists/<id>"
 * @param  {Object}   data      JSON data to send in request body
 * @param  {function} onSuccess   callback method to execute upon request success (200 status)
 * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
 * @return {None}
 */
var makePostRequest = function (url, data, onSuccess, onFailure) {
    $.ajax({
        type: 'POST',
        url: apiUrl + url,
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
        success: onSuccess,
        error: onFailure
    });
};

var playlist_format = function (ppd, title, length, id) {
    return "<div onclick='playlistHandler()' id='" + id + "'class='playlist'><li><img src='" + ppd + "' style=\"width: 100px; height: 100px\"><b class='playlist_title'>" + title + "</b> <i>" + length + " songs</i></li></div>";
};

var track_format = function (title, artist, album) {
    return "<li><div class='track'><b class='track_title'>" + title + "</b> - <i>" + artist + "</i> - <i>" + album + "</i> </div> </li>";
};

var followHandler = function () {
    var id = $('.follow').prop('id');

    var onPostSuccess = function (data) {
        makeGetRequest('/api/profiles/following/' + id, onGetFollowingSuccess, onFailure);
        makeGetRequest('/api/profiles/followers/' + id, onGetFollowersSuccess, onFailure);
    }
    
    var onGetFollowingSuccess = function (data) {
        if (data.following != null) {
            $('.following').text(data.following);
        } else {
            $('.following').text('None');
        }
    }
    
    var onGetFollowersSuccess = function (data) {
        if (data.followers != null) {
            $('.followers').text(data.followers); 
        } else {
            $('.followers').text('None');
        }
    }

    var onFailure = function (data) {
        console.error('Follow/Unfollow - Failed')
    }

    makePostRequest('/api/profiles/follow/' + id, null, onPostSuccess, onFailure);
};

var playlistHandler = function () {
    $('div.playlist').click(function() {
        $(".track_list").html('<img src="https://media2.giphy.com/media/17mNCcKU1mJlrbXodo/giphy.gif"/>');
        
        var onSuccess = function (data) {
            $('.track_list').html('');
            
            for(var i = 0; i < data.tracks.length; i++) {
                $('.track_list').append(track_format(data.tracks[i].track.name, data.tracks[i].track.artists[0].name, data.tracks[i].track.album.name))
            }
        }

        var onFailure = function (data) {
            console.error('Display Playlist - Failed')
        }

        makeGetRequest('/api/playlist/' + $(this).prop('id'), onSuccess, onFailure);
    });
};

var displayMyPlaylists = function () {
    $(".playlist_list").html('<img src="https://media2.giphy.com/media/17mNCcKU1mJlrbXodo/giphy.gif"/>');

    var onSuccess = function (data) {
        $(".playlist_list").html('');

        for (var i = 0; i < data.playlists.length; i++) {
            $(".playlist_list").append(playlist_format(data.playlists[i].images[0].url, data.playlists[i].name, data.playlists[i].tracks.total, data.playlists[i].id));
        }        
    }

    var onFailure = function (data) {
        console.error('List all Playlists - Failed');
    }

    makeGetRequest('/api/playlists/me', onSuccess, onFailure);
};

var displayPlaylists = function(id) {
    $(".playlist_list").html('');

    var onSuccess = function(data) {
        for (var i = 0; i < data.playlists.length; i++) {
            $(".playlist_list").append(playlist_format(data.playlists[i].images[0].url, data.playlists[i].name, data.playlists[i].tracks.total));
        }       
    }

    var onFailure = function(data) {
        console.error('List all Playlists - Failed'); 
    }

    makeGetRequest('/api/playlists/' + id, onSuccess, onFailure);
};
