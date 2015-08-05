

$(document).ready(function() {


/* 
01. HTML5 MEDIA ________________________________________________________________ */
$('audio,video').mediaelementplayer({
	success: function(player, node) {
		$('#' + node.id + '-mode').html('mode: ' + player.pluginType);
	}
});
		
     
// End Call	 
});



