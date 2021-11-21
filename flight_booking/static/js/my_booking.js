function popup(element) {
    let ref = element.dataset.ref;
    document.querySelector("#cancel_ticket_btn").dataset.ref = ref;
    document.querySelector(".popup").style.display = 'block';
}

function remove_popup() {
    document.querySelector(".popup").style.display = 'none';
    document.querySelector("#cancel_ticket_btn").dataset.ref = "";
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


$(document).ready( function () {
    $('#btnPdf').click(function () {
        if ($('#txt_ticketID').val() == '') {
            alert ('ยังไม่ระบุุ ticket_id');
            return false;
        }
        window.open('/ticket/pdf/' + $('#txt_ticketID').val());
    });
});