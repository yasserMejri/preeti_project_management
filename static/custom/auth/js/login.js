$("#login-form").validate({
    rules: {
        username: {
            required: true,
            minlength: 5
        },
        password: {
			required: true,
			minlength: 5
		},
    },
    errorElement : 'div',
    errorPlacement: function(error, element) {
      var placement = $(element).data('error');
      if (placement) {
        $(placement).append(error)
      } else {
        error.insertAfter(element);
      }
    }
 });
