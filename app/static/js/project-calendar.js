document.addEventListener('DOMContentLoaded', function() {
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: "/projects/" + project_id + "/events/get",
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    locale: 'pl',
    firstDay: 1,
    selectable: true,
    select: function(selectionInfo) {
        var title = prompt('Event Title:');
        var eventData;
        if (title) {
            console.log("Title:", title);
            console.log("Start:", selectionInfo.startStr);
            console.log("End:", selectionInfo.endStr);
            let str = calendar.formatIso('2018-09-01');
            console.log(str);
            //console.log(selectionInfo.allDay);

            let date_end = new Date(selectionInfo.endStr);
            if(selectionInfo.allDay){
              date_end.setDate(date_end.getDate() - 1);
            }
            console.log(date_end.toISOString());
            //$('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
            // Send new event data to the server
            var all_day = 1;
            if(selectionInfo.startStr.length > 10){
                all_day = 0;
            }

            $.ajax({
                url: '/projects/' + project_id + '/events/store',
                type: 'POST',
                data:{
                    "title": title,
                    "start": calendar.formatIso(selectionInfo.startStr),
                    "end": calendar.formatIso(date_end.toISOString()),
                    "all-day": all_day
                },
                success: function(response) {
                    console.log('Event added successfully:', response);
                    calendar.refetchEvents();
                },
                error: function(xhr, status, error) {
                    console.error('Error adding event:', error);
                    alert('Error: ' + status);
                }
            });
        }
        //$('#calendar').fullCalendar('unselect');
    },

    eventClick: function(info) {
        


        // Populate modal with event data
        console.log(info);
        let date_end = new Date(info.event.endStr);
        date_end.setDate(date_end.getDate() - 1);
        console.log(date_end.toISOString());
        document.getElementById('eventTitle').value = info.event.title;
        document.getElementById('eventLocation').value = info.event.extendedProps.location;
        document.getElementById('eventTravelTime').value = info.event.extendedProps.travel_time;
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
            


            var all_day = 1;
            if(info.event.startStr.length > 10){
                all_day = 0;
                date_end.setHours(date_end.getHours() + 1);
            }else{
                date_end.setDate(date_end.getDate() + 1);
            }
            console.log(date_end.toISOString());
            info.event.setProp('title', document.getElementById('eventTitle').value);
            info.event.setStart(document.getElementById('eventStart').value);
            info.event.setEnd(date_end.toISOString().slice(0, 16));
            info.event.setExtendedProp("location", document.getElementById('eventLocation').value)
            info.event.setExtendedProp("travel_time", document.getElementById('eventTravelTime').value)
            
            if(all_day == 0){
                //date_end = new Date(info.event.endStr);
                date_end.setHours(date_end.getHours() - 1);
                console.log(date_end.toISOString());
            }else{
                //date_end = new Date(info.event.endStr);
                date_end.setDate(date_end.getDate() - 1);
                console.log(date_end.toISOString());
            }
            
            
            // Use AJAX to save the changes to the server
            $.ajax({
            url: '/projects/' + project_id + '/events/update', // Replace with your endpoint
            type: 'POST',
            data: {
                id: info.event.id,
                title: info.event.title,
                start: calendar.formatIso(info.event.start),
                end: calendar.formatIso(date_end.toISOString()),
                all_day: all_day,
                location: info.event.extendedProps.location,
                travel_time: info.event.extendedProps.travel_time
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