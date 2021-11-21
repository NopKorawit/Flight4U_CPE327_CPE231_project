function popup(element) {
    let ticket_id = element.dataset.ticket_id;
    document.querySelector("#cancel_ticket_btn").dataset.ticket_id = ticket_id;
    document.querySelector(".popup").style.display = 'block';
}

function remove_popup() {
    document.querySelector(".popup").style.display = 'none';
    document.querySelector("#cancel_ticket_btn").dataset.ticket_id = "";
}

function cancel_tkt() {
    let ticket_id = document.querySelector("#cancel_ticket_btn").dataset.ticket_id;
    let formData = new FormData();
    formData.append('ticket_id',ticket_id)
    fetch('ticket/cancel',{
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(response => {
        if (response.success === true) {
            remove_popup();
            document.querySelector(`[id='${ticket_id}'] .ticket-action-div`).innerHTML = '';
            document.querySelector(`[id='${ticket_id}'] .status-div`).innerHTML = `<div class="red">CANCELLED</div>`;
            document.querySelector(`[id='${ticket_id}'] .booking-date-div`).innerHTML = '';
        }
        else {
            remove_popup();
            alert(`Error: ${response.error}`)
        }
    });
}