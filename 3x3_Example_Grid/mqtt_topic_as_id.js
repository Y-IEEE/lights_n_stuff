// BOARD INFO
var rows = 3;
var cols = 3;
var lights = [0,0,0,0,0,0,0,0,0];

// MQTT INFO
var connected = false;
var host = "farmer.cloudmqtt.com";
var port = 34479;
var client_id = "lightboard_" + parseInt(Math.random() * 100, 10);
var usr = "xoemllsy";
var pass = "hdgazSRFNst3";

// MISC INFO
var red = "#D8554B";
var green = "#64B743"
var blue = "#4BAED8";

// CONVERT AN RGB ARRAY OF NUMBERS TO AN ARRAY OF STRINGS WHICH EACH ONE CORRESPONDING TO THAT LIGHT
function number_to_color_array(number_array) {
    var color_array = [];
    for(var i = 0; i < (rows * cols); i++) {
        switch(number_array[i]) {
            case 0:
                color_array.push("000000");
                break;
            case 1:
                color_array.push("ff0000");
                break;
            case 2:
                color_array.push("00ff00");
                break;
            case 3:
                color_array.push("0000ff");
                break;
        }
    }

    return color_array;
}

// Create a client instance
client = new Paho.MQTT.Client(host, port, client_id);
    //Example client = new Paho.MQTT.Client("m11.cloudmqtt.com", 32903, "web_" + parseInt(Math.random() * 100, 10));

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;
    var options = {
        useSSL: true,
        userName: usr,
        password: pass,
        onSuccess: onConnect,
    onFailure:doFail
}

// connect the client
client.connect(options);

    // called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("Connect success");
    document.getElementById("messages").innerHTML += '<span><b> Connected To:</b><br> <em>' + host + '</em> on port <em>' + port + '</em> with id <em>' + client_id + '</em></span>';
    client.subscribe("/cloudmqtt"); // TOPIC
    message = new Paho.MQTT.Message("new connection"); // MESSAGE
    message.destinationName = "/cloudmqtt";
    connected = true;
    // client.send(message); //no mesage just know succesful connection
}

function doFail(e) {
    connected = false;
    console.log(e);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    connected = false;
        if (responseObject.errorCode !== 0) {
            document.getElementById("messages").innerHTML += '<br><span><b> Connection Lost:</b><br> ' + responseObject.errorMessage + '</span>';
            console.log("Connection Lost: "+responseObject.errorMessage);
        }
}

// called when a message arrives
function onMessageArrived(message) {
    console.log("Message Delivered: " + message.payloadString);	
    document.getElementById("messages").innerHTML += '<br><span><b> Message Delivered:</b><br> ' + message.payloadString + '</span>';
}

function clicked(id) {
    var finalMessage = "";
    switch(lights[id]) {
        case 0:
            lights[id] = 1;
            document.getElementById("button-"+id).style.background = red;
            break;
        case 1:
            lights[id] = 2;
            document.getElementById("button-"+id).style.background = green;
            break;
        case 2:
            lights[id] = 3;
            document.getElementById("button-"+id).style.background = blue;
            break;
        default:
            lights[id] = 0;
            document.getElementById("button-"+id).style.background = "white";
            break;
    }

    colorsArray = number_to_color_array(lights);

    // console.log("Sent: " + lights);
    if(connected == true) {
        console.log("Button Clicked");
        for(var i = 0; i < colorsArray.length; i++) {
            client.subscribe(i.toString().padStart(3, '0')); // TOPIC
            message = new Paho.MQTT.Message(colorsArray[i]); // MESSAGE
            message.destinationName = i.toString().padStart(3, '0'); //TOPIC
            console.log("Sending message to topic: " + i.toString().padStart(3, '0'));	
            document.getElementById("messages").innerHTML += '<br><span><b> Sending Message To Topic:</b><br> ' + i.toString().padStart(3, '0') + '</span>';
            client.send(message);
        }
        
    } else {
        location.reload();
    }
}
