function deleteFile(file_element, file_id, file_name){
    if(confirm("Delete file " + file_name + "?")){
        $.ajax({
            url: '/projects/' + project_id + '/files/delete/' + file_id.toString(),
            type: 'POST',
            data:{
                "file_id": file_id,
            },
            success: function(response) {
                file_element.remove();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });
    }
}

function updateFile(file_id, file_name, file_name_element){
    file_name = prompt("New file name: ", file_name);
    if(file_name != null && file_name != ""){
        $.ajax({
            url: '/projects/' + project_id + '/files/update/' + file_id.toString(),
            type: 'POST',
            data:{
                "file_id": file_id,
                "file_name": file_name
            },
            success: function(response) {
                file_name_element.html(file_name);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });
    }
}

$(document).on('click', '.file-delete', function() {
    console.log("test");
    var fileElement = $(this).closest('.file-item');
    var fileId = fileElement.data('id');
    var fileName = fileElement.data('name');
    deleteFile(fileElement, fileId, fileName);
});

$(document).on('click', ".file-change-name", function() {
    var fileElement = $(this);
    var fileId = fileElement.data('id');
    var fileName = fileElement.data('name');
    console.log(fileId);
    updateFile(fileId, fileName, fileElement);
});