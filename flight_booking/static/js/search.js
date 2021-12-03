function flight_search() {
    let select_depart = document.getElementById("js_Departure");
    let index_depart = select_depart.selectedIndex;
    let select_dest = document.getElementById("js_Destination");
    let index_dest = select_dest.selectedIndex;

    if (index_depart == 0) {
        alert("Please select a departure city.")
        return false;
    }
    if (index_dest == 0) {
        alert("Please select a destination city.")
        return false;
    }
    else{
        return true;
    }

}