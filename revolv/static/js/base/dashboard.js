$(document).ready(function() {
	$('.accordion-navigation').click(function() {
		var active = $(this).find(".content").hasClass("active");
		$('.accordion li div').removeClass("active")
		if (!active){
			var liItem = $(this);
			$('.accordion li div').removeClass("active")
			var href = $(this).find("div").addClass("active");
		}
	});

	$('.status-bar').hover(function() {
		$(".status-bar").removeClass('active');
		$(this).addClass('active');
		$(this).css("background-color", "white");
		$(this).find(".status-bar-menu-text").css("color", "$revolv-header-color");
	}, function() {
		$(".status-bar").removeClass('active');
		$(this).css("background-color", "");
		$(this).find(".status-bar-menu-text").css("color", "white");
	});

	doOverlay();

});

var doOverlay = function() {
	
	/**
	* Go through each overlay on top of each project image
	* and add a transparent top to bottom black gradient to each one.
	*/

	$(".overlay").each(function() {
		var item = $(this);
		item.css("width", "100%");
		item.css("height", "100%");
		item.css("top", "0");
		item.css("left", "0");
		item.css("position", "absolute");
		item.css("background", "linear-gradient(to bottom, rgba(0, 0, 0, .05),  rgba(0, 0, 0, .3))");
	});
}
