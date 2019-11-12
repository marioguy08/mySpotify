var apiUrl = 'http://localhost';

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
    return "<div onclick='playlistHandler(\""+id+"\")' id='" + id + "' class='playlist'><li><img src='" + ppd + "' class='playlist-cover'><b class='playlist-title'>" + title + "</b> - <i>" + length + " songs</i></li></div>";
};

var track_format = function (title, artist, album) {
    return "<li><div class='track'><b class='track-title'>" + title + "</b> - <i>" + artist + "</i> - <i>" + album + "</i></div></li>";
};

var followHandler = function () {
    var id = $('.follow').prop('id');

    var onPostSuccess = function (data) {
        makeGetRequest('/api/profile/following/' + id, onGetFollowingSuccess, onFailure);
        makeGetRequest('/api/profile/followers/' + id, onGetFollowersSuccess, onFailure);
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

    makePostRequest('/api/profile/follow/' + id, null, onPostSuccess, onFailure);
};

var playlistHandler = function (playlist_id) {
    $(".track-list").html('<div class="loading-div"><img class="loading" src="../static/img/loading.gif"/></div>');
    
    var onSuccess = function (data) {
        $('.track-list').html('');
        
        for(var i = 0; i < data.tracks.length; i++) {
            $('.track-list').append(track_format(data.tracks[i].track.name, data.tracks[i].track.artists[0].name, data.tracks[i].track.album.name))
        }
    }

    var onFailure = function (data) {
        console.error('Display Playlist - Failed')
    }
    
    console.log(playlist_id);

    makeGetRequest('/api/playlist/' + playlist_id, onSuccess, onFailure);
};

var statusHandler = function () {
    var onSuccess = function(data) {
        $('.status-content').text(data.status);
    }

    var onFailure = function(xhr, status, error) {
        alert(xhr.responseText);
    }
    
    var data = { 'status' : $('.status-input').val() };
    makePostRequest('/api/profile/me/status', data, onSuccess, onFailure);
};

var displayMyPlaylists = function () {
    $(".playlist-list").html('<div class="loading-div"><img class="loading" src="../static/img/loading.gif"/></div>');

    var onSuccess = function (data) {
        $(".playlist-list").html('');

        for (var i = 0; i < data.playlists.length; i++) {
            $(".playlist-list").append(playlist_format(data.playlists[i].images[0].url, data.playlists[i].name, data.playlists[i].tracks.total, data.playlists[i].id));
        }        
    }

    var onFailure = function (data) {
        console.error('List all Playlists - Failed');
    }

    makeGetRequest('/api/playlists/me', onSuccess, onFailure);
};

var displayPlaylists = function(id) {
    $(".playlist-list").html('');

    var onSuccess = function(data) {
        for (var i = 0; i < data.playlists.length; i++) {
            $(".playlist-list").append(playlist_format(data.playlists[i].images[0].url, data.playlists[i].name, data.playlists[i].tracks.total));
        }       
    }

    var onFailure = function(data) {
        console.error('List all Playlists - Failed'); 
    }

    makeGetRequest('/api/playlists/' + id, onSuccess, onFailure);
};
