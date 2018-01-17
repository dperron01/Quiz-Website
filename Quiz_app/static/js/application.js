
$(function() {
    $('#process_input').click(function(e) {
        $.ajax({
            url: '/admin/topic_approval',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(data) {
                console.log(data);
            }
        });
        e.preventDefault();
	});
    $.ajaxSetup({
    	beforeSend: function(xhr, settings){
    		if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
    			xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}")
    		}
    	}
    })
});