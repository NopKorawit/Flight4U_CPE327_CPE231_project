// let register = document.getElementById('register');
// let email = document.getElementById('email');
// let phone_no = document.getElementById('phone_no');
// let password = document.getElementById('password');
// let repassword = document.getElementById('repassword');
// let register_btn = document.getElementById('btn');

//จะ disable ปุ่ม ถ้ากรอกไม่ครบอะ แต่ทำไม่ได้

// document.addEventListener("DOMContentLoaded", () => {
//     let check = [false,false,false,false,false,false];
//     document.querySelectorAll(".inp").forEach(input => {
//         input.addEventListener('input', () => {

//             if(input.classList.contains('usrname')){
//                 if(input.value.trim().length !== 0) {check[0]=true;}
//                 else{check[0] = false;}
//             }
//             if(input.classList.contains('fname')){
//                 if(input.value.trim().length !== 0) {check[1]=true;}
//                 else{check[1] = false;}
//             }
//             if(input.classList.contains('lname')){
//                 if(input.value.trim().length !== 0) {check[2]=true;}
//                 else{check[2] = false;}
//             }
//             if(input.classList.contains('pswd')){
//                 document.querySelector('.cpswd').value = "";
//                 document.querySelector('.cpswd').parentElement.querySelector('span').innerText = "";
//                 check[4] = false;
//                 if(input.value.trim().length !== 0) {check[3]=true;}
//                 else{check[3] = false;}
//             }
//             if(input.classList.contains('cpswd')){
//                 if(input.value.trim().length !== 0) {
//                     if(input.value !== document.querySelector('.pswd').value) {
//                         input.parentElement.querySelector('span').innerText = "Password must match";
//                         check[4] = false;
//                     }
//                     else {
//                         input.parentElement.querySelector('span').innerText = "";
//                         check[4]=true;
//                     }
//                 }
//                 else{check[4] = false;}
//             }
//             if(input.classList.contains('email')){
//                 if(input.value.trim().length !== 0) {check[5]=true;}
//                 else{check[5] = false;}
//             }

//             let i;
//             for(i=0;i<6;i++) {
//                 if(!check[i]) {
//                     break;
//                 }
//             }

//             if(i===6) {
//                 document.querySelector('input[type="submit"]').disabled = false;
//             }
//             else {
//                 document.querySelector('input[type="submit"]').disabled = true;
//             }

//         });
//     });
// });