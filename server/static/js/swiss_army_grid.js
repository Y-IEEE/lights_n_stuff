// WEBSOCKET INFO
var connected = false;
const socket = io();

// // COLOR WHEEL STUFF
var colorWheel = new iro.ColorPicker("#colorWheel", {

    layout: [{
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
        }
    ],

    layoutDirection: "horizontal"

});

// event listeners
function dim_submit_func() {
    if (connected) {
        var width = $('#dim_width').val()
        var height = $('#dim_height').val()

        // make sure the numbers are legit
        if (width == NaN || height == NaN || width < 1 || height < 1) {
            console.log("bad input")
            return
        }

        console.log("submitting new grid dimensions")
        socket.emit("client_dim_submit", { 'width': width, 'height': height })
    } else {
        location.reload()
    }

}



socket.on('connect', function() {
    console.log("Socket client connected!")
    connected = true;


});

// update grid from server messages
socket.on("server_update_light", function(data) {
    var id = data.id;
    var color = data.color;

    console.log("Light callback received!");
    console.log(data);

    document.getElementById("button-" + parseInt(id)).style.background = color;
})

// construct the grid
socket.on("create_grid", function(data) {
    var width = data.width
    var height = data.height

    console.log(`Constructing grid of dim [${width}, ${height}]`)


    $(document).ready(function() {
        var gridBody = $('#light_grid')

        // clear the grid of any previous entities
        gridBody.empty()

        for (i = 0; i < height; i++) {
            for (j = 0; j < width; j++) {
                // add the tile
                var buttonNum = (i * width) + j
                var buttonToAdd = `<button id="button-${buttonNum}">${buttonNum}</button>`
                var buttonDom = $(buttonToAdd).appendTo(gridBody)

                buttonDom.on('click', function(buttonDomWrap, buttonNumWrap) {
                    return function() {
                        if (connected == true) {
                            console.log("Button Clicked");

                            console.log("Color: " + colorWheel.color.hexString);
                            buttonDomWrap.css('background', colorWheel.color.hexString);
                            socket.emit("client_update_light", { "id": buttonNumWrap, "color": colorWheel.color.hexString }); // should ID be the same as mqtt topic for consistency?

                        } else {
                            location.reload();
                        }
                    }
                }(buttonDom, buttonNum))

            }
            gridBody.append('<br>')
        }
    })

})