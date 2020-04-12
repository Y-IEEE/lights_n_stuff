// BOARD INFO
var rows = 3;
var cols = 3;
var lights = Array(rows*cols).fill("#000000");

// WEBSOCKET INFO
var connected = false;
const socket = io();


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
            socket.emit("lights", {"id": (id%cols).toString().padStart(2, '0') + "x" + Math.floor(id/cols).toString().padStart(2, '0'), "color": lights[i].substring(1)});
            console.log("Sending \"" + lights[i].substring(1) + "\" to topic: " + (id%cols).toString().padStart(2, '0') + "x" + Math.floor(id/cols).toString().padStart(2, '0'));	
        }
        
    } else {
        location.reload();
    }
}
