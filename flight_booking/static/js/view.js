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