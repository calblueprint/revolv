$(document).ready(function(){
	$('.accordion-navigation').click(function(){
		console.log("clicked");
		var active = $(this).find("div").hasClass("active");
		$('.accordion li div').removeClass("active")
		if (!active){
			var liItem = $(this);
			$('.accordion li div').removeClass("active")
			var href = $(this).find("div").addClass("active");
		}
	});

	$('.status-bar').hover(function(){
		console.log("hovered");
		$(".status-bar").removeClass('active');
		$(this).addClass('active');
		//$(this).css("border-color", "$revolv-header-color");
		$(this).css("background-color", "white");
		$(this).find(".status-bar-menu-text").css("color", "$revolv-header-color");
	}, function() {
		console.log("unhovered");
		$(".status-bar").removeClass('active');
		//$(this).css("border-color", "");
		$(this).css("background-color", "");
		$(this).find(".status-bar-menu-text").css("color", "white");
	});

	doOverlay();

});

var doOverlay = function(){
	$(".overlay").each(function(){
		console.log("overlay");
		var item = $(this);
		item.css("width", "100%");
		item.css("height", "100%");
		item.css("top", "0");
		item.css("left", "0");
		item.css("position", "absolute");
		item.css("background", "linear-gradient(to bottom, rgba(0, 0, 0, .05),  rgba(0, 0, 0, .3))");
	});
}


var fillInProgressBars = function(){
	//handle getting percentages
	console.log('hi')
	var first = 70;
	var second = 30;
	var third = 10;
	var fourth = 100;
	var arr = [first, second, third, fourth]

	// //var greenBars = document.getElementByClassName('.green-bar');

	// for (var i = 0; i < arr.length; i+=1){
	// 	greenBars[i].css("width", arr[i]+"%");
	// }
}

fillInProgressBars();