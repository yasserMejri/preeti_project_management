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
	$("#timelimit").change(function() {
		$("#timelimit-value").text($(this).val() + 'mins');
	}); 

	$("#detail-card").hide();
	$(".experiment").click(function() {
		var data = exp_data[$(this).attr('data-id')]
		console.log(data)
		$("#detail-name").text(data['name'] + " Experiment Details")
		$("#detail-dataset").text(data['dataset'])
		var algos = '<ul class="algo-list">';
		for(algo in data['algorithms'])
			algos += '<li class="algo-item"> <span>'+algo+'</span> </li>';
		algos += '</ul>';
		$("#detail-algorithms").html(algos);
		$("#detail-metric").text(data['metric']);
		$("#detail-validation").text(data['validation']); 
		$("#detail-tuning").text(data['tuning']);
		$("#detail-timelimit").text(data['timelimit'] + ' minutes'); 
		$("#detail-description").text(data['description']);

		$("#detail-card").show();
	}); 

	$("#validator-select").parent().hide();
	$("#validation-select").change(function() {
		if($(this).val() == 'Seperate Dataset') {
			$("#validator-select").parent().show();
			$("#validation-parameter").hide();
		} else {
			$("#validator-select").parent().hide();
			$("#validation-parameter").show();
		}
	}); 
}); 
