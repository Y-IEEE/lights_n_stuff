// BOARD INFO
var rows = 3;
var cols = 3;
var lights = [0,0,0,0,0,0,0,0,0];

// WEBSOCKET INFO
var connected = false;
const socket = io();


// MISC INFO
var red = "#D8554B";
var green = "#64B743"
var blue = "#4BAED8";

// // COLOR WHEEL STUFF
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

socket.on('connect', function() {
    console.log("Socket client connected!")
    connected = true;


});



function clicked(id) {

    colorsArray = number_to_color_array(lights);
    console.log(colorsArray);
    // console.log("Sent: " + lights);
    if(connected == true) {
        console.log("Button Clicked");

        console.log("Color: " + colorWheel.color.hexSstring);
        document.getElementById("button-"+ parseInt(id)).style.background = colorWheel.color.hexSstring;
        socket.emit("client_update_light", {"id": id, "color": colorWheel.color.hexSstring});
        
    } else {
        location.reload();
    }
}

// add event listeners
window.onload = function() {
    for (var i = 0; i < 9; i++) {
        document.getElementById("button-"+ parseInt(i)).addEventListener("click", clicked(i));
    }
}


socket.on("server_update_light", function(data) {
    var id = data.id;
    var color = data.color;

    console.log("Light callback received!");
    console.log(data);

    document.getElementById("button-"+ parseInt(id)).style.background = color;
})




