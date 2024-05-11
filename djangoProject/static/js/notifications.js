function deleteNotification(notificationId) {
    if (confirm("Вы уверены, что хотите удалить это уведомление?")) {
        fetch(`/delete_notification/${notificationId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
            },
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error('Failed to delete notification');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function markAsViewed(notificationId) {
    fetch(`/mark_as_viewed/${notificationId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                console.error('Failed to mark notification as viewed');
            }
        })
        .catch(error => console.error('Error:', error));
}
function deleteAllNotifications(event) {
    if (confirm("Вы уверены, что хотите удалить все уведомления?")) {
        fetch('/delete_all_notifications/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
        })
            .then(response => {
                if (response.ok) {
                    alert('Все уведомления успешно удалены.');
                    location.reload();
                } else {
                    console.error('Failed to delete all notifications');
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        event.preventDefault();
        console.log('Отменено удаление всех уведомлений.');
    }
}


function markAllAsViewed(event) {
    if (confirm("Вы уверены, что хотите просмотреть все уведомления?")) {
        fetch('/mark_all_as_viewed/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
        })
            .then(response => {
                if (response.ok) {
                    alert('Все уведомления отмечены как просмотренные.');
                    location.reload();
                } else {
                    console.error('Failed to mark all notifications as viewed');
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        event.preventDefault();
        console.log('Отменено просмотр всех уведомлений.');
    }
}
