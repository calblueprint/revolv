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

	fillInProgressBars();
});

function fillInProgressBars(){
	//first
	
	//second
	//third
	//fourth
}