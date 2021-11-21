
document.addEventListener('DOMContentLoaded', () => {
    flight_duration();
});

function flight_duration() {
    document.querySelectorAll(".duration").forEach(element => {
        let time = element.dataset.value.split(":");
        if(time[1] == 0){
            element.innerText = time[0]+" hr";
        }
        else{
            element.innerText = time[0]+" hr "+time[1]+" min";
        }
        
    });
}


$(document).ready(function(){

    let btnAdd = document.getElementById('btnAdd');
    let i = 0;
    let max_p = 9;
    if(i<max_p){
        i++
        btnAdd.addEventListener('click',(e)=>{
            console.log('Add')
            e.preventDefault();
            displayDetails(i);
    })
    }


})

function displayDetails(num_p) {

    console.log('display Add')
    let fname = document.getElementById('fname').value;
    let lname = document.getElementById('lname').value;
    let email = document.getElementById('่js_email').value;
    let phone = document.getElementById('phone').value;
    let idno = document.getElementById('idno').value;

    if(!fname || !lname || !email || !phone){
        alert('Please enter all the form');
        return;
    }

    if( /^[A-Za-z]+$/.test(fname)==false && /^[A-Za-z]+$/.test(lname)==false){
        alert('Please enter your name correctly');
        return;
    }

    if(ValidateEmail(email)==false){
        return;
    }

    if(phonenumber(phone)==false){
        return;
    }

    if(validateID(idno)==false){
        return;
    }

    if(validateName(fname)==false || validateName(lname)==false){
        return;
    }

    else{

    let plist = document.getElementById('plist');
    let count_p = document.querySelectorAll(".passenger-list .addP").length;
    console.log(count_p);
    passenger = `
    <div class="row addP">
        <div class="show-p col-3">
            <span class="p-name">${fname}&nbsp;&nbsp;${lname}</span><span>,</span>
            <span class="p-email">${email}</span>
        </div> 
        <input type="hidden" name="fname${count_p+1}" value="${fname}">
        <input type="hidden" name="lname${count_p+1}" value="${lname}">
        <input type="hidden" name="email${count_p+1}" value="${email}">
        <input type="hidden" name="idno${count_p+1}" value="${idno}">
        <input type="hidden" name="phone${count_p+1}" value="${phone}">
        <button class="btn fas fa-times col-2" type="button" onclick="del_passenger(this)"></button>
    `;

    // <div class="p_email col-3" name="pemail${count_p+1}">${email}</div>
    //     <div class="p_email col-3" name="pemail${count_p+1}">${email}</div>
    //     <div class="p_email col-3" name="pemail${count_p+1}">${email}</div>


    plist.innerHTML+= passenger
    document.querySelector("#p-count").value = count_p+1;
    document.querySelector(".p-head h6 span").innerText = count_p+1;
    document.getElementById("totalP").innerText = count_p+1;
    console.log(count_p);
    re_calculate_total_price();
    clearForm();
    }

//-------------------------------------------------------------------------



//-------------------------------------------------------------------------

}

function clearForm() {
    let form = document.querySelector(".input-content");
    let inputs = form.querySelectorAll("input");
    inputs.forEach((input) => input.value = '');
}

function del_passenger(btn) {
    console.log('del')
    let passenger = btn.parentElement; 
    let psg = btn.parentElement.parentElement.parentElement;
    let cnt = psg.querySelector("#p-count");
    cnt.value = parseInt(cnt.value)-1;
    console.log(cnt.value)
    document.querySelector(".p-head h6 span").innerText = cnt.value;
    document.getElementById("totalP").innerText = cnt.value;
    console.log(cnt.value)
    passenger.remove();
    re_calculate_total_price();
}

function book_submit() {
    let pcount = document.querySelector("#p-count");
    if(parseInt(pcount.value) > 0) {
        return true;
    }
    alert("Please add at least one passenger.")
    return false;
}

//---------------------------------------------------------------

function re_calculate_total_price () {
    var total_price = 0;
    console.log("recalculating total price")
    var basefare = document.getElementById("baseFare").innerHTML;
    console.log(basefare);
    var totalP = document.getElementById("totalP").innerHTML;
    console.log(totalP);
    if (totalP != "") {
        var total_price = basefare * totalP;
        $(this).find(".total-amount").html(formatNumber(total_price));
    }

    $('#lbl_Fee').text(formatNumber(total_price * 0.07));
    $('#txt_VAT').val($('#lbl_Fee').text());
    $('#lbl_TotalAmount').text(formatNumber(total_price * 1.07));
    $('#total_amount').val($('#lbl_TotalAmount').text());
    
}

// ---------------------------------------------------------------

function ValidateEmail(mail) 
{
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
    {
        return (true)
    }
    alert("You have entered an invalid email address!")
    return (false)
}

function phonenumber(number)
{
    var phoneno = /^\d{10}$/;
    if(number.match(phoneno)){
        return true;
    }
    else{
        alert("You have entered an invalid phone number!");
        return false;
    }
}

function validateID(idno)
{
        var passport = /^[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]$/;
        var idcard = /^\d{13}$/;
        
        if(passport.test(idno) == true || idno.match(idcard))
        {
            return true;
        }
        else
        {   alert("You have entered an invalid Passport/ID card number!");
            return false;
            
        }
}

function validateName(name)
{
    if (/[^a-zA-Z0-9\-]/.test(name)){
        alert("Family name can only contain alphanumeric characters and hypehns(-)")
        return false;
    }
    
    return true;
}

function formatNumber (num) {
    if (num === '') return '0';
    num = parseFloat(num); 
    return num.toFixed(2).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
}

//---------------------No use----------------------------

function lineitem_to_json() {
    var rows = [];
    var i = 0;
    $("#table_main tbody tr").each(function (index) {
        if ($(this).find('.project_code_1 > span').html() != '') {
            rows[i] = {};
            rows[i]["item_no"] = (i + 1);
            rows[i]["product_code"] = $(this).find('.project_code_1 > span').html();
            rows[i]["product_name"] = $(this).find('.product_name').html();
            rows[i]["unit_price"] = $(this).find('.unit_price').html();
            rows[i]["quantity"] = $(this).find('.quantity').html();
            rows[i]["product_total"] = $(this).find('.product_total').html();
            i++;
        }
    });
    var obj = {};
    obj.lineitem = rows;
    //console.log(JSON.stringify(obj));

    return JSON.stringify(obj);
}

function get_ticket_detail (ticket_id) {
    $.ajax({
        url:  '/ticket/detail/' + encodeURIComponent(ticket_id),
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            //console.log(data.ticketlineitem.length);

            reset_table();
            for(var i=ROW_NUMBER;i<data.ticketlineitem.length;i++) {
                $('.table-add').click();
            }
            var i = 0;
            $("#table_main tbody tr").each(function() {
                if (i < data.ticketlineitem.length) {
                    $(this).find('.first_name').html(data.ticketlineitem[i].first_name);
                    $(this).find('.last_name').html(data.ticketlineitem[i].last_name);
                    $(this).find('.phone_no').html(data.ticketlineitem[i].phone_no);
                    $(this).find('.email').html(data.ticketlineitem[i].email);
                }
                i++;
            });
            re_calculate_total_price();
        },
    });
}

// $(document).ready(function () {
//     $('#btnSave').click(function () {
//         if ($('#txt_ticketNo').val() == '<new>') {
//             var token = $('[name=csrfmiddlewaretoken]').val();

//             $.ajax({
//                 url: '/ticket/create',
//                 type: 'post',
//                 data: $('#form_ticket').serialize() + "&lineitem=" + lineitem_to_json(),
//                 headers: { "X-CSRFToken": token },
//                 dataType: 'json',
//                 success: function (data) {
//                     if (data.error) {
//                         alert(data.error);
//                     } else {
//                         $('#txt_ticketNo').val(data.ticket.ticket_id)
//                         alert('บันทึกสำเร็จ');
//                     }
//                 },
//             });
//         }
        // } else {
        //     var token = $('[name=csrfmiddlewaretoken]').val();
        //     console.log($('#form_ticket').serialize());
        //     console.log(lineitem_to_json());
        //     $.ajax({
        //         url: '/ticket/update/' + $('#txt_ticketNo').val(),
        //         type: 'post',
        //         data: $('#form_ticket').serialize() + "&lineitem=" + lineitem_to_json(),
        //         headers: { "X-CSRFToken": token },
        //         dataType: 'json',
        //         success: function (data) {
        //             if (data.error) {
        //                 alert(data.error);
        //             } else {
        //                 alert('บันทึกสำเร็จ');
        //             }
        //         },
        //     });
        // }

//     });
// });