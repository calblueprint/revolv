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

});

function fillInProgressBars(){
	//handle getting percentages
	console.log('hi')
	var first = 70;
	var second = 30;
	var third = 10;
	var fourth = 100;
	var arr = [first, second, third, fourth]

	var greenBars = document.getElementByClassName('.green-bar');

	for (var i = 0; i < arr.length; i+=1){
		greenBars[i].css("width", arr[i]+"%");
	}
}

fillInProgressBars();