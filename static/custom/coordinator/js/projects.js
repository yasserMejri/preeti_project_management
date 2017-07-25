$(document).ready(function() {
	$("#delete-btn").click(function() {
		$(this).toggleClass('delete');
		$(".item").toggleClass('delete');
	}); 
	$(".item.delete").click(function() {
		alert('delete item');
		return false;
	}); 
}); 
