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

	$('.tab-item').click(function(){
		$('.tab').removeClass("active");
		$('.tab-item').removeClass("active");
		
		$(this).addClass("active");
		var ref = $(this).find('a').attr('href');
		console.log(ref);
		$(ref).addClass('active');
	});
});