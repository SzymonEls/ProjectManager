const project_id = 0;
document.addEventListener('DOMContentLoaded', function() {
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: "/projects/0/events/get",
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    locale: 'pl',
    firstDay: 1,
    eventClick: function(info) {
        


        // Populate modal with event data
        console.log(info);
        let date_end = new Date(info.event.endStr);
        date_end.setDate(date_end.getDate() - 1);
        console.log(date_end.toISOString());
        document.getElementById('eventTitle').value = info.event.title;
        document.getElementById('project-name').innerHTML = '<a href="' + info.event.extendedProps.project_url +  '">' + info.event.extendedProps.project_name + '</a>';
        if(info.event.allDay == false){
            document.getElementById('eventStart').type = "datetime-local";
            document.getElementById('eventEnd').type = "datetime-local";
            document.getElementById('eventStart').value = info.event.startStr.slice(0,16);
            document.getElementById('eventEnd').value = info.event.endStr.slice(0,16);
        }else{
            document.getElementById('eventStart').type = "date";
            document.getElementById('eventEnd').type = "date";
            document.getElementById('eventStart').value = info.event.startStr.slice(0,10);
            document.getElementById('eventEnd').value = date_end.toISOString().slice(0,10);
        }
        
        
        
        
        // Open modal
        var myModal = new bootstrap.Modal(document.getElementById('eventModal'));
        myModal.show();

        // Handle save button
        document.getElementById('saveEvent').onclick = function() {
            //console.log(info);
            let date_end = new Date(document.getElementById('eventEnd').value);
            date_end.setDate(date_end.getDate() + 1);
            console.log(date_end.toISOString());
            info.event.setProp('title', document.getElementById('eventTitle').value);
            info.event.setStart(document.getElementById('eventStart').value);
            info.event.setEnd(date_end.toISOString().slice(0, 16));


        var all_day = 1;
        if(info.event.startStr.length > 10){
            all_day = 0;
        }

            date_end = new Date(info.event.endStr);
            date_end.setDate(date_end.getDate() - 1);
            console.log(date_end.toISOString());
            
            // Use AJAX to save the changes to the server
            $.ajax({
            url: '/projects/' + project_id + '/events/update', // Replace with your endpoint
            type: 'POST',
            data: {
                id: info.event.id,
                title: info.event.title,
                start: calendar.formatIso(info.event.start),
                end: info.event.end ? calendar.formatIso(date_end.toISOString()) : null,
                all_day: all_day
            },
            success: function(response) {
                console.log('Event updated successfully');
            },
            error: function(xhr, status, error) {
                console.error('Error updating event:', error);
            }
            });

            myModal.hide();
        };

        // Handle delete button
        document.getElementById('deleteEvent').onclick = function() {
            if(confirm("Do you want to delete event " + info.event.title + "?")){
                

                // Use AJAX to delete the event from the server
                $.ajax({
                    url: '/projects/' + project_id + '/events/delete', // Replace with your endpoint
                    type: 'POST',
                    data: {
                    id: info.event.id
                    },
                    success: function(response) {
                    console.log('Event deleted successfully');
                    info.event.remove();
                    },
                    error: function(xhr, status, error) {
                    console.error('Error deleting event:', error);
                    }
                });
    
                myModal.hide();
            }
            
        };
    }
});
calendar.render();
});