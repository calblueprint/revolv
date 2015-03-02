$(document).ready(function(){
	$("#donate-button").hover(function(){
		//console.log('hovering')
		$(this).addClass("hover");
	}, function(){
		$(this).removeClass("hover")
	});

	$("#donate-button").click(function(){
		$(this).find('a').click();
	});
});