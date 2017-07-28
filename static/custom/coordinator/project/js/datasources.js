$(document).ready(function() {
	$("#file-input").change(function() {
		$("#filename").text($(this).val());
	}); 
});