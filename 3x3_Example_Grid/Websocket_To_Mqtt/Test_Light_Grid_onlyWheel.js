// BOARD INFO
var rows = 3;
var cols = 3;
var lights = Array(rows*cols).fill("#000000");

// WEBSOCKET INFO
var connected = false;
const socket = io();


// MISC INFO
var red = "#D8554B";
var green = "#64B743"
var blue = "#4BAED8";

// COLOR WHEEL STUFF
var colorWheel = new iro.ColorPicker("#colorWheel", {

    layout: [
    { 
      component: iro.ui.Wheel,
      options: {
        wheelLightness: true,
        wheelAngle: 0,
        wheelDirection: "anticlockwise"
      } 
    },
    {
      component: iro.ui.Box,
      options: {
        // see below
      }
    },
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'hue', // can also be 'saturation', 'value', 'alpha' or 'kelvin',
        sliderShape: 'circle'
      }
    }
    ]
  
});


socket.on('connect', function() {
    socket.emit("info", "Socket Client Connected!");
    connected = true;
});



function clicked(id) {
    var finalMessage = "";
    var wheelHex = (colorWheel.color.hexString);
    document.getElementById("button-"+id).style.background = wheelHex;
    lights[id] = wheelHex;

    colorsArray = number_to_color_array(lights);
    console.log(lights);
    // console.log("Sent: " + lights);
    if(connected == true) {
        for(var i = 0; i < lights.length; i++) {
            var id = i.toString().padStart(3, '0');
            socket.emit("lights", {"id": id, "color": lights[i].substring(1)});
            // client.subscribe(i.toString().padStart(3, '0')); // TOPIC
            // message = new Paho.MQTT.Message(colorsArray[i]); // MESSAGE
            // message.destinationName = i.toString().padStart(3, '0'); //TOPIC
            console.log("Sending \"" + lights[i].substring(1) + "\" to topic: " + id);	
            // document.getElementById("messages").innerHTML += '<br><span><b> Sending Message To Topic:</b><br> ' + id + '</span>';
            // client.send(message);
        }
        
    } else {
        location.reload();
    }
}
