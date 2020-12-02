// GRID INFO
var currentWidth
var currentHeight
var gridFrames = []
var currentFrameNum = 0

var offToggle = false
var OFF_COLOR = "#EFEFEF"

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

function nextFrame() {
    // save current grid status to gridFrames[currentFrame]
    isNewFrame = (currentFrameNum == gridFrames.length)

    if (isNewFrame) {
        gridFrames[currentFrameNum] = []
    }

    for (i = 0; i < currentHeight; i++) {

        new_row = []

        for (j = 0; j < currentWidth; j++) {
            buttonID = String(j).padStart(2, 0) + "x" + String(i).padStart(2, 0)
            buttonDom = $('#button-' + buttonID)
            buttonCol = buttonDom.css('background')

            if (isNewFrame) {
                // making a new frame
                buttonDom.css('background', OFF_COLOR)
                new_row[j] = OFF_COLOR
            } else {
                // next frame already exists
                buttonDom.css('background', gridFrames[currentFrameNum][i][j])
            }

        }

        if (isNewFrame) {
            gridFrames[currentFrameNum].push(new_row)
        }
    }

    currentFrameNum += 1
    $('#frame_id').text("Current Frame: " + currentFrameNum)
}

function prevFrame() {
    if (currentFrameNum > 1) {


        for (i = 0; i < currentHeight; i++) {
            for (j = 0; j < currentWidth; j++) {
                buttonID = String(j).padStart(2, 0) + "x" + String(i).padStart(2, 0)
                buttonDom = $('#button-' + buttonID)

                // set color to previous frame
                buttonDom.css('background', gridFrames[currentFrameNum - 2][i][j])
            }
        }

        currentFrameNum -= 1
        $('#frame_id').text("Curent Frame: " + currentFrameNum)
    }
}

function toggleOffSwitch() {
    offToggle = !offToggle
}


// setup the grid
function initGrid(width, height) {

    // make sure the numbers are legit
    if (width == NaN || height == NaN || width < 1 || height < 1) {
        console.log("bad input")
        return
    }

    // init all grid-related variables
    currentWidth = width
    currentHeight = height
    gridFrames = []
    currentFrameNum = 0

    // init the frame
    nextFrame()

    console.log(`creating new grid with dimensions [${width}, ${height}]`)

    var gridBody = $('#light_grid')

    // clear the grid of any previous entities
    gridBody.empty()

    for (i = 0; i < height; i++) {
        for (j = 0; j < width; j++) {
            // add the tile
            var buttonNum = (i * width) + j
            var buttonID = String(j).padStart(2, 0) + "x" + String(i).padStart(2, 0)
            var buttonToAdd = `<button class="grid_button" id="button-${buttonID}">${buttonNum}</button>`
            var buttonDom = $(buttonToAdd).appendTo(gridBody)

            buttonDom.on('click', function(buttonDomWrap, buttonIDWrap, iWrap, jWrap) {
                return function() {
                    console.log("Button Clicked");
                    if (offToggle) {
                        buttonDomWrap.css('background', OFF_COLOR)
                        gridFrames[currentFrameNum - 1][iWrap][jWrap] = OFF_COLOR
                    } else {
                        console.log("Color: " + colorWheel.color.hexString);
                        buttonDomWrap.css('background', colorWheel.color.hexString);
                        gridFrames[currentFrameNum - 1][iWrap][jWrap] = colorWheel.color.hexString
                    }


                }
            }(buttonDom, buttonID, i, j))

        }
        gridBody.append('<br>')
    }

    $('#grid_title').text(width + "x" + height + " Light Grid Animation Canvas")

}


function exportGrid() {
    a = []

    // push size
    a.push(String(currentWidth).padStart(2, 0) + "x" + String(currentHeight).padStart(2, 0) + "\n")

    // push fps and animation marker
    a.push("10\n---\n")


    for (i = 0; i < gridFrames.length; i++) {
        for (j = 0; j < currentHeight; j++) {
            for (k = 0; k < currentWidth; k++) {
                a.push(gridFrames[i][j][k] + ' ')
            }
            a.push('\n')
        }
        a.push('\n')
    }

    animationText = a.join('')
    console.log(animationText)
    $('#animation_output').text("Succesful! Check console")

}

$(document).ready(function() {
    initGrid(5, 5)
})