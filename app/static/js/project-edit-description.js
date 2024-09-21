$(document).ready( function(){
    var displayText = document.getElementById('displayText');
    displayText.innerHTML = marked.parse(project_status_text)
});

function toggleEditMode() {
    var displayText = document.getElementById('displayText');
    var editText = document.getElementById('editText');
    var editableTextarea = document.getElementById('editableTextarea');



    if (editText.style.display === 'none') {
        editableTextarea.value = project_status_text;
        displayText.style.display = 'none';
        editText.style.display = 'block';
    } else {
        displayText.style.display = 'block';
        editText.style.display = 'none';
    }
}

function saveText() {
    var displayText = document.getElementById('displayText');
    var editableTextarea = document.getElementById('editableTextarea');

    status_text_new = editableTextarea.value
    project_status_text = status_text_new;

    $.ajax({
            url: '/projects/' + project_id + '/update',
            type: 'POST',
            data:{
                "status_text": status_text_new
            },
            success: function(response) {
                displayText.innerHTML = marked.parse(status_text_new);
                toggleEditMode();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });

    
    
}
