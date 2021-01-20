var sol = 0;


size = 8

// draw canvas
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.clearRect(0, 0, c.width, c.height);
length = c.width / 1
square_length = length/size

window.onload() = draw_board(a)
window.onload() = flip_this()

function prev(a){
    sol -= 1
    draw_board(a)
    flip_this()
}


function next(a){
    sol += 1
    draw_board(a)
    flip_this()

}


function flip_this() {
    console.log('sol ' + sol)
    document.getElementById("ans").innerHTML ="Sol " + (sol + 1) ;
}

function draw_board(a) {
    ctx.clearRect(0, 0, c.width, c.height);
    for (let i = 0; i <= length; i+= length/size) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, length);
    
        ctx.stroke();
    }
  
    for (let i = 0; i <= length; i+= length/size) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(length, i);
        ctx.stroke();
    }
    console.log(a[sol])

    board = add_eight(a[sol])

    draw_targets(board)

}

function draw_target(x, y, l) {
    ctx.font = length/7 + "px Arial";
    ctx.fillText("H", x*l, (y+1)*l);
}


function add_eight(array) {

    for (let i = 1; i < array.length; i++) {
        array[i] = array[i] + (i*size)
    }
    console.log(array)
    board = new Array(size * size)
    for (let i = 0; i < board.length; i++) {
        if(array.includes(i)) {
            board[i] = 1
            // console.log(i)
        } else {
            board[i] = 0
        }
    }
    return board
}

function draw_targets(dict) {
    for (let i = 0; i < size * size; i++) {
        if (dict[i] == 1) {
            x = i%size
            y = Math.floor(i/size)
            console.log(x, y)

            draw_target(y,x,square_length)
        }
    }
}


