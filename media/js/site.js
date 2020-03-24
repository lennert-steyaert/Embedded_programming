// Global variable

var window;
var windowNumber;


function postDevice(dev) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/polls/webios", true);
    //xhr.setRequestHeader('X-CSRF-Token', token);
    xhttp.setRequestHeader("Content-type", "application/json");
    var data = JSON.stringify({"pk":dev});
    xhttp.onreadystatechange = function() {
        if ( xhttp.readyState == XMLHttpRequest.DONE) {
            $('#DetailView').html(xhttp.responseText);
        }
    }
    xhttp.send(data);
}

function reloadDevices() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/polls/webdevices", true);
    xhttp.onreadystatechange = function() {
        if ( xhttp.readyState == XMLHttpRequest.DONE) {
            $('#DevicesView').html(xhttp.responseText);
        }
    }
    xhttp.send();
}

function updateTextInput(name,val) {
    console.log(name.id)
    document.getElementById(name.id).value=val; 
}

// Put io
function ValidateForm(pk,device){
    var text = document.getElementById("textinput"+pk);
    var integer = document.getElementById("integerinput"+pk);
    var decimal = document.getElementById("decimalinput"+pk);
    console.log(pk);
    console.log(text.value);
    console.log(integer.value);
    console.log(decimal.value);

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/polls/webputio", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    var data = JSON.stringify({"pk":pk,"device":device,"IO":{"stateInteger":integer.value,"stateText":text.value,"stateDecimal":decimal.value}});
    xhttp.onreadystatechange = function() {
        if ( xhttp.readyState == XMLHttpRequest.DONE) {
            console.log("DONE")
            updateInput(pk)
        }
    }
    xhttp.send(data);
}

function checkRefresh(id,pk) {
    result = document.getElementById(id).checked;
    if(result){
        startInterval(pk)
    }
    else{
        stopInterval(pk)
        console.log("stop")
    }
    console.log(id);
    console.log(pk);
    console.log(result);
}

function startInterval(pk){
    console.log(pk)
    window['p'+pk] = setInterval(updateInput, 500,pk) /* time in milliseconds (ie 2 seconds)*/
}

// Get io NO NONE EXCEPION
function updateInput(pk){
    console.log("update"+pk)
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/polls/webgetio", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    var data = JSON.stringify({"id":pk});
    xhttp.onreadystatechange = function() {
        if ( xhttp.readyState == XMLHttpRequest.DONE) {
            //$('#DetailView').html(xhttp.responseText);
            // first layer
            var myObj = JSON.parse(this.responseText);
            var obj_pk = myObj[0].pk
            var obj_device = myObj[0].device
            var obj_io = myObj[0].IO
            // second layer
            var obj_integer = obj_io.stateInteger
            var obj_text = obj_io.stateText
            var obj_decimal = obj_io.stateDecimal

            document.getElementById("textinput"+pk).value = obj_text;
            document.getElementById("integerrange"+pk).value = obj_integer;
            document.getElementById("integerinput"+pk).value = obj_integer;
            document.getElementById("decimalinput"+pk).value = obj_decimal;
            console.log(myObj[0])            
        }
    }
    xhttp.send(data);
 }

function stopInterval(pk){
    console.log(pk)
    clearInterval(window['p'+pk]);
}