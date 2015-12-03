function showRequestContact(formData, jqForm, options2) { 
	var form = jqForm[0];
	var validRegExp = /^[^@]+@[^@]+.[a-z]{2,}$/i;
	
	if (!form.name.value) { 
		$('#output-contact').html('<div class="output2">Please fill the Name field!</div>'); 
		return false; 
	} else if (!form.email.value) {
		$('#output-contact').html('<div class="output2">Please fill the Email field!</div>'); 
		return false; 
	} else if (form.email.value.search(validRegExp) == -1) {
		$('#output-contact').html('<div class="output2">Please provide a valid Email address!</div>'); 
		return false; 
	}
	else if (!form.subject.value) {
		$('#output-contact').html('<div class="output2">Please fill the Subject field!</div>'); 
		return false; 
	}
	else if (!form.message.value) {
		$('#output-contact').html('<div class="output2">Please fill the Message field!</div>'); 
		return false; 
	}
	 else {	   
	 $('#output-contact').html('Sending message...!');  		
		return true;
	}
}