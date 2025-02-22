function starProject(project_star_element, project_id){
    $.ajax({
        url: '/projects/' + project_id + '/star',
        type: 'POST',
        data:{
            "project_id": project_id,
        },
        success: function(response) {
            var status = ["Star", "Starred"]
            if(response["starred"]){
                project_star_element.html("Starred");
            }else{
                project_star_element.html("Star");
            }
            
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Error: ' + status);
        }
    });
}

$(document).on('click', '.star-project', function() {
    var projectStarElement = $(this);
    var projectId = projectStarElement.data('id');
    starProject(projectStarElement, projectId);
});