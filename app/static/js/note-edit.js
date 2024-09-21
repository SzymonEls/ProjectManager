$(document).ready( function(){
    var displayText = document.getElementById('displayText');
    displayText.innerHTML = marked.parse(note_content);
});

function toggleEditMode() {
    var displayText = document.getElementById('displayText');
    var editText = document.getElementById('editText');
    var editableTextarea = document.getElementById('editableTextarea');

    if (editText.style.display === 'none') {
        editableTextarea.value = note_content;
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

    var content_new = editableTextarea.value;
    note_content = content_new; 

    $.ajax({
            url: '/projects/' + project_id + '/notes/update',
            type: 'POST',
            data:{
                "note_id": note_id,
                "content": content_new
            },
            success: function(response) {
                displayText.innerHTML = marked.parse(content_new);
                toggleEditMode();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });

    
    
}

document.addEventListener('DOMContentLoaded', (event) => {
    const editableDiv = document.getElementById('edit-note-name');
    let flag = false; // A flag to track whether the event was handled by keydown

    function save() {
        let new_note_name = editableDiv.innerHTML;
        console.log(new_note_name);
        $.ajax({
            url: '/projects/' + project_id + '/notes/update',
            type: 'POST',
            data:{
                "note_id": note_id,
                "name": new_note_name
            },
            success: function(response) {
                
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });	
    }

    editableDiv.addEventListener('blur', () => {
        if (!flag) {
            save();
        }
        flag = false;
    });

    editableDiv.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); //No new line in a field
            save();
            flag = true;
            editableDiv.blur(); // Removes focus
        }
    });
});