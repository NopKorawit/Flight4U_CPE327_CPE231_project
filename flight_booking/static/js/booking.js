document.addEventListener('DOMContentLoaded', () => {
    flight_duration();
});

function flight_duration() {
    document.querySelectorAll(".duration").forEach(element => {
        let time = element.dataset.value.split(":");
        if (time[1] == 0) {
            element.innerText = time[0] + " hr";
        } else {
            element.innerText = time[0] + " hr " + time[1] + " min";
        }

    });
}

$(document).ready(function () {

    let btnAdd = document.getElementById('btnAdd');
    let i = 0;
    let max_p = 9;
    if (i < max_p) {
        i++
        btnAdd.addEventListener('click', (e) => {
            console.log('Add')
            e.preventDefault();
            displayDetails();
        })
    }
})

function displayDetails() {

    console.log('display Add')
    let fname = document.getElementById('fname').value;
    let lname = document.getElementById('lname').value;
    let email = document.getElementById('่js_email').value;
    let phone = document.getElementById('phone').value;
    let idno = document.getElementById('idno').value;

    if (!fname || !lname || !email || !phone) {
        alert('Please enter all the form');
        return;
    }

    if (/^[A-Za-z]+$/.test(fname) == false && /^[A-Za-z]+$/.test(lname) == false) {
        alert('Please enter your name correctly');
        return;
    }

    if (ValidateEmail(email) == false) {
        return;
    }

    if (ValidatePhone(phone) == false) {
        return;
    }

    if (ValidateID(idno) == false) {
        return;
    }

    if (ValidateName(fname) == false || ValidateName(lname) == false) {
        return;
    } else {

        let plist = document.getElementById('plist');
        let count_p = document.querySelectorAll(".passenger-list .addP").length;
        console.log(count_p);
        passenger = `
    <div class="addP">
        <div class="show-p row">
            <div class="p-name col-4">${fname}&nbsp;&nbsp;${lname}</div><span class="col-1">,</span>
            <div class="p-email col-6">${email}</div>
            <button class="btn fas fa-times col-1" type="button" onclick="del_passenger(this)"></button>
        </div> 
        <input type="hidden" name="fname${count_p+1}" value="${fname}">
        <input type="hidden" name="lname${count_p+1}" value="${lname}">
        <input type="hidden" name="email${count_p+1}" value="${email}">
        <input type="hidden" name="idno${count_p+1}" value="${idno}">
        <input type="hidden" name="phone${count_p+1}" value="${phone}">
    </div>
    `;

        plist.innerHTML += passenger
        document.querySelector("#p-count").value = count_p + 1;
        document.querySelector(".p-head h6 span").innerText = count_p + 1;
        document.getElementById("totalP").innerText = count_p + 1;
        console.log(count_p);
        re_calculate_total_price();
        clearForm();
    }



}

function clearForm() {
    let form = document.querySelector(".input-content");
    let inputs = form.querySelectorAll("input");
    inputs.forEach((input) => input.value = '');
}

function del_passenger(btn) {
    console.log('del')
    let passenger = btn.parentElement.parentElement;
    // console.log('passenger = '+ passenger.className);
    let psg = btn.parentElement.parentElement.parentElement.parentElement;
    // console.log('psg = '+ psg.className);
    let cnt = psg.querySelector("#p-count");
    cnt.value = parseInt(cnt.value) - 1;

    document.querySelector(".p-head h6 span").innerText = cnt.value;
    document.getElementById("totalP").innerText = cnt.value;
    passenger.remove();
    re_calculate_total_price();
}

function book_submit() {
    let pcount = document.querySelector("#p-count");
    if (parseInt(pcount.value) > 0) {
        return true;
    }
    alert("Please add at least one passenger.");
    return false;
}

//---------------------------------------------------------------

function re_calculate_total_price() {
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
    $('#txt_TotalAmount').val($('#lbl_TotalAmount').text());

}

// ---------------------------------------------------------------
function ValidateEmail(mail) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)) {
        return true;
    } else {
        alert("You have entered an invalid email address!");
        return false;
    }
}

function ValidatePhone(number) {
    var phoneno = /^\d{10}$/;
    if (number.match(phoneno)) {
        return true;
    } else {
        alert("You have entered an invalid phone number!");
        return false;
    }
}

function ValidateID(idno) {

    if (idno.length > 9) {
        return true;
    } else {
        alert("You have entered an invalid Passport/ID card number!");
        return false;

    }
}

function ValidateName(name) {
    if (/[^a-zA-Z0-9\-]/.test(name)) {
        alert("Family name can only contain alphanumeric characters and hypehns(-)")
        return false;
    }

    return true;
}

function formatNumber(num) {
    if (num === '') return '0';
    num = parseFloat(num);
    return num.toFixed(2).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
}
