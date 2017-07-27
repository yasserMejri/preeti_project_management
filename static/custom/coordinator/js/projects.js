$(document).ready(function() {
	$("#delete-btn").click(function() {
		$(this).toggleClass('delete');
		$(".item").toggleClass('delete');
	}); 
	$(".item.delete").click(function() {
		alert('delete item');
		return false;
	}); 
	$(".edit-btn").click(function() {
		var idx = parseInt($(this).attr('data')); 
		var p_data = projects_data[idx];
		console.log(projects_data[idx]);
		$("#edit-project-name").val(p_data["name"]);
		$("#edit-project-note").val(p_data['description']);
		$("#edit-visibility").val(p_data['visibility']); 
		$("#edit-task").val(p_data['task']); 
		$("#edit-category").val(p_data['category']);
		$("#edit-pid").val(idx);

		$("#edit-visibility").material_select();
		$("#edit-task").material_select();
		$("#edit-category").material_select();
	}); 
	$(".delete-btn").click(function() {
		var btn = $(this)
	    swal({    title: "Are you sure?",
            text: "You will not be able to recover this project!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Yes, delete it!",   
            closeOnConfirm: true }, 
            function(){   
				var elem = $(btn).parentsUntil('.item');
				$.post(window.location,  {
					'csrfmiddlewaretoken': csrf, 
					'project_id': $(btn).attr('data'), 
					'delete': true
				}, function(r) {
					var data = JSON.parse(r);
					if(data.status == 'success') {
						Materialize.toast('Deleted!', 2000);
						elem.remove();
					} else {
						Materialize.renderToStaticMarkup()
					}
				});
				return false;
            });
	}); 
}); 
