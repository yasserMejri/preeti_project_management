$(document).ready(function() {
	$("#submit-form").hide();
	$(".next-step").click(function() {
		var active = $(".step.active"); 
		if($(active).next('.step').next('.step').length == 0) {
			$(this).hide();
			$("#submit-form").show();
		} 
		if($(active).next('.step').length != 0) {
			$(active).next('.step').toggleClass('active');
			$(active).toggleClass('active');
		}
	});
	$(".back-step").click(function() {
		var active = $(".step.active"); 
		console.log(active.prev('.step'));
		if($(active).prev('.step').length != 0) {
			$('.next-step').show();
			$("#submit-form").hide();
			$(active).prev('.step').toggleClass('active');
			$(active).toggleClass('active');
		}
	}); 
}); 
