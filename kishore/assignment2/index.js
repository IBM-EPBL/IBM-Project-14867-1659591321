function Validate () {
    let table=document.getElementById('table');
    var row = table.insertRow(0);

   //var name = row.insertCell(0);
    var email = row.insertCell(0);
    var pass = row.insertCell(1);
    var radio = row.insertCell(2);
    var drop = row.insertCell(3);
    var textarea = row.insertCell(4);

    //name.innerHTML = document.getElementById("fname").value;
    email.innerHTML = document.getElementById("email").value;
    pass.innerHTML =document.getElementById("pass").value;
    radio.innerHTML = document.getElementById("fav_language").value;
    drop.innerHTML = document.getElementById("cars").value;
    textarea.innerHTML = document.getElementById("tarea").value;


    alert("success");
    
    return false;
}
