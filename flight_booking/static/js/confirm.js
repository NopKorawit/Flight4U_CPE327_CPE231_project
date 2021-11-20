
$(document).ready( function () {
    $('#btnPdf').click(function () {
        if ($('#txt_ticketID').val() == '') {
            alert ('ยังไม่ระบุุ ticket_id');
            return false;
        }
        window.open('/ticket/pdf/' + $('#txt_ticketID').val());
    });
});