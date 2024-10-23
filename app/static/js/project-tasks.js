function addTask() {
    var taskName = document.getElementById('newTaskName').value;
    var taskDate = document.getElementById('newTaskDate').value;

    if (taskName && taskDate) {
        $.ajax({
            url: '/projects/' + project_id + '/tasks/store',
            type: 'POST',
            data:{
                "name": taskName,
                "date": taskDate
            },
            success: function(response) {
                var taskList = document.querySelector('.task-list');
                var newTask = document.createElement('div');
                newTask.classList.add('task-item');

                var taskNameSpan = document.createElement('span');
                taskNameSpan.setAttribute('contenteditable', 'true');
                taskNameSpan.textContent = taskName;

                var taskDateDiv = document.createElement('div');
                taskDateDiv.classList.add('task-date');
                var taskDateInput = document.createElement('input');
                taskDateInput.setAttribute('type', 'date');
                taskDateInput.setAttribute('value', taskDate);
                taskDateDiv.appendChild(taskDateInput);

                newTask.appendChild(taskNameSpan);
                newTask.appendChild(taskDateDiv);
                taskList.appendChild(newTask);

                // Reset form fields
                document.getElementById('newTaskName').value = '';
                document.getElementById('newTaskDate').value = '';
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });
        
    } else {
        alert('Proszę wprowadzić nazwę zadania i datę.');
    }
}

function starTask(task_star_element, task_id){
    $.ajax({
        url: '/projects/' + project_id + '/tasks/star',
        type: 'POST',
        data:{
            "task_id": task_id,
        },
        success: function(response) {
            var status = ["Star", "Starred"]
            if(response["starred"]){
                task_star_element.html("Starred");
            }else{
                task_star_element.html("Star");
            }
            
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Error: ' + status);
        }
    });
}

function deleteTask(task_element, task_id, task_name){
    if(confirm("Delete task " + task_name + "?")){
        $.ajax({
            url: '/projects/' + project_id + '/tasks/delete',
            type: 'POST',
            data:{
                "task_id": task_id,
            },
            success: function(response) {
                task_element.remove();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error: ' + status);
            }
        });
    }
}

function updateTask(task_id, task_date, task_name){
    $.ajax({
        url: '/projects/' + project_id + '/tasks/' + task_id.toString() + '/update',
        type: 'POST',
        data:{
            "task_id": task_id,
            "task_date": task_date,
            "task_name": task_name
        },
        success: function(response) {

        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Error: ' + status);
        }
    });
}

$(document).on('click', '.star-task', function() {
    var taskStarElement = $(this);
    var taskId = taskStarElement.data('id');
    starTask(taskStarElement, taskId);
});

$(document).on('click', '.delete-task', function() {
    var taskElement = $(this).closest('.task-item');
    var taskId = taskElement.data('id');
    var taskName = taskElement.data('name');
    deleteTask(taskElement, taskId, taskName);
});

$(document).on('change', ".task-change-date", function() {
    var taskElement = $(this).closest('.task-item');
    var taskId = taskElement.data('id');
    var task_date = $(this).val();
    updateTask(taskId, task_date, "");
});

$(document).on('keypress', '.task-name', function(e) {
    if (e.which == 13) {
        e.preventDefault(); // No new line
        $(this).blur();
    }
});

$(document).on('blur', '.task-name', function() {
    const taskItem = $(this).closest('.task-item');
    const taskId = taskItem.data('id');
    const taskName = $(this).text().trim();
    console.log(taskId);
    // AJAX request to update task name
    updateTask(taskId, "", taskName);
});