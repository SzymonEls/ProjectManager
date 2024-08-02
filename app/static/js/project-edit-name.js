document.addEventListener('DOMContentLoaded', (event) => {
    const editableDiv = document.getElementById('edit-project-name');
    let flag = false; // A flag to track whether the event was handled by keydown

    function save() {
        let new_project_name = editableDiv.innerHTML;
        console.log(new_project_name);
        $.ajax({
            url: '/projects/' + project_id + '/update',
            type: 'POST',
            data:{
                "name": new_project_name
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