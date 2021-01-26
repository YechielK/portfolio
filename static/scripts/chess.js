// TODO: fix shwoing target binary


// draw canvas
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.clearRect(0, 0, c.width, c.height);
length = c.width / 1
square_length = length/8


target_orig = 0
var flip_dec

window.onload = draw_board(length)
ctx.stroke();


// which squares on boards are heads
dict = []

// values to be displayed
vals = []

random_dict()
draw_targets(dict)

board = board_parity(dict)
window.onload = result()

flip_this(board, target_orig)

update_ans()

// for code
c.addEventListener('click', (e) => {
  const pos = {
    x: e.clientX,
    y: e.clientY

  };
// console.log(pos)
var rect = c.getBoundingClientRect();
x_offset = rect.left
y_offset = rect.top


x = Math.floor((pos.x - x_offset)/(length/8))
y = Math.floor((pos.y - y_offset)/(length/8))
t = (x + 1) + ((y) * 8)
t = t-1
// console.log(t)

if (t > 63) {  
} else if (dict[t] == 1) {
  dict[t] = 0
} else {
  dict[t] = 1
}


ctx.clearRect(0, 0, c.width, c.height);
draw_board(length)
draw_targets(dict)


board = board_parity(dict)
var target_dec = target_orig
flip_this(board, target_dec)


console.log(vals)

update_ans()



});

function update_ans() {
    document.getElementById("col_zero").innerHTML = '2^0 = ' + vals['col_zero']  + ' = ' + vals['col_zero_parity'] 
    document.getElementById("col_one").innerHTML =  '2^1 = ' + vals['col_one'] + ' = ' + vals['col_one_parity']
    document.getElementById("col_two").innerHTML =  '2^2 = ' + vals['col_two'] + ' = ' + vals['col_two_parity']
    document.getElementById("row_three").innerHTML= '2^3 = ' + vals['row_three'] + ' = ' + vals['row_three_parity']
    document.getElementById("row_four").innerHTML = '2^4 = ' + vals['row_four'] + ' = ' + vals['row_four_parity']
    document.getElementById("row_five").innerHTML = '2^5 = ' + vals['row_five'] + ' = ' + vals['row_five_parity']
    document.getElementById("board_parity").innerHTML = 'Board ' +  vals['board_parity']
    document.getElementById("target_bin").innerHTML = 'Target ' + vals['target_bin']
    document.getElementById("flip_bin").innerHTML ='Flip ' + vals['flip_bin']
}


function random_dict(){
  for (let i = 0; i < 64; i++) {
    dict[i] = Math.floor(Math.random() * Math.floor(2))
  }
}

function draw_board(length) {
    for (let i = 0; i <= length; i+= length/8) {
    
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, length);
  
    ctx.stroke();
  }
  
  for (let i = 0; i <= length; i+= length/8) {
  
  ctx.beginPath();
  ctx.moveTo(0, i);
  ctx.lineTo(length, i);
  
  ctx.stroke();
  }

  draw_things()


  
  }


function draw_targets(dict) {
    for (let i = 0; i < 64; i++) {
        if (dict[i] == 1) {
            x = i%8
            y = Math.floor(i/8)
            draw_target(x,y,square_length)
        }
    }
}


function draw_things() {
  for (let i = 0; i < 64; i++) {
          x = i%8
          y = Math.floor(i/8)
          draw_number(x,y,square_length,i)
  }
}



function flip_this(board, target_dec) {
target_bin = num_to_binary(parseInt(target_dec))
target_bin = padding(target_bin)
flip_bin = flip(board,target_bin)
console.log('flip ' + flip_bin)
console.log('target ' + target_bin)
vals['flip_bin'] = flip_bin
vals['target_bin'] = target_bin
flip_dec = parseInt(flip_bin, 2)
document.getElementById("ans").innerHTML ="Flip " + flip_dec;
}


function padding(binary) {
  while(binary.length < 6) {
    binary = '0' + binary
  }
  return binary
}

function result() {
  board = board_parity(dict)
  target_orig = document.getElementById("text").value;
  console.log('res ' + target_orig)
  flip_this(board, target_orig)
  update_ans()
}

function flip(board, target) {
  ans = ''
  for (let i = 0; i < target.length; i++) {
    if (board[i] == target[i]) {
      ans += '0'
    } else {
      ans += '1'
    }
    
  }
  return ans
}

function clear_dict(dict) {
  for (let i = 0; i < 64; i++) {
    dict[i] = 0
  }
}

function clear_board() {
  clear_dict(dict)
  ctx.clearRect(0, 0, c.width, c.height)
  draw_board(length)

  board = board_parity(dict)
  target_dec = target_orig
  flip_this(board, target_dec)
  update_ans()
}

function random_board() {
  clear_board(length)
  random_dict()
  draw_targets(dict)
  board = board_parity(dict)
//   document.getElementById("ans").innerHTML ="Flip " + flip_dec;
  flip_this(board, target_orig)
update_ans()

}

function row_sum(dict, s) {
  sum = 0
  for (let i = 0; i < 8; i++) {
    sum += dict[(s*8) + i]
  }
  return sum
}

function col_sum(dict, s) {
  sum = 0
  for (let i = s; i < 64; i+=8) {
    //first cols
    sum += dict[i]
  }
  return sum
}

function sum_cols(dict, cols) {
    sum = 0
    for (let i = 0; i < a.length; i++) {
        sum += col_sum(dict, cols[i])
    }
    return sum
}

function sum_rows(dict, rows) {
    sum = 0
    for (let i = 0; i < a.length; i++) {
        sum += row_sum(dict, rows[i])
    }
    return sum
}


function board_parity(dict) {

    a = [0,2,4,6]
    b = [0,1,4,5]
    cs = [0,1,2,3]

    col_zero = sum_cols(dict, a)
    col_one = sum_cols(dict, b)
    col_two = sum_cols(dict, cs)

    row_three = sum_rows(dict, a)
    row_four = sum_rows(dict, b)
    row_five = sum_rows(dict, cs)


    vals['col_zero'] = col_zero
    vals['col_one'] = col_one
    vals['col_two'] = col_two
    vals['row_three'] = row_three
    vals['row_four'] = row_four
    vals['row_five'] = row_five

    
    if (dict.reduce((a, b) => a + b, 0)%2 == 0) {
      str = ''
      str += col_zero%2
      str += col_one%2
      str += col_two%2
      str += row_three%2
      str += row_four%2
      str += row_five%2
      console.log(col_zero)
      console.log(col_one)
      console.log(col_two)
      console.log(row_three)
      console.log(row_four)
      console.log(row_five)

      console.log(col_zero%2)
      console.log(col_one%2)
      console.log(col_two%2)
      console.log(row_three%2)
      console.log(row_four%2)
      console.log(row_five%2)

      vals['col_zero_parity'] = col_zero%2
      vals['col_one_parity'] = col_one%2
      vals['col_two_parity'] = col_two%2
      vals['row_three_parity'] = row_three%2
      vals['row_four_parity'] = row_four%2
      vals['row_five_parity'] = row_five%2

    
    } else {
      str = ''
      str += ((col_zero%2)+1)%2
      str += ((col_one%2)+1)%2
      str += ((col_two%2)+1)%2
      str += ((row_three%2)+1)%2
      str += ((row_four%2)+1)%2
      str += ((row_five%2)+1)%2
      console.log(col_zero)
      console.log(col_one)
      console.log(col_two)
      console.log(row_three)
      console.log(row_four)
      console.log(row_five)


      console.log(((col_zero%2)+1)%2)
      console.log(((col_one%2)+1)%2)
      console.log(((col_two%2)+1)%2)
      console.log(((row_three%2)+1)%2)
      console.log(((row_four%2)+1)%2)
      console.log(((row_five%2)+1)%2)

      vals['col_zero_parity'] = ((col_zero%2)+1)%2
      vals['col_one_parity'] = ((col_one%2)+1)%2
      vals['col_two_parity'] = ((col_two%2)+1)%2
      vals['row_three_parity'] = ((row_three%2)+1)%2
      vals['row_four_parity'] = ((row_four%2)+1)%2
      vals['row_five_parity'] = ((row_five%2)+1)%2

    }
    ans = str.split("").reverse().join("")
    console.log( 'board parity ' + ans)
    vals['board_parity'] = ans
    // console.log(col_zero)
    // console.log(col_one)
    // console.log(col_two)
    // console.log(row_three)
    // console.log(row_four)
    // console.log(row_five)
    
    // console.log(col_zero)
    // console.log(col_one)
    // console.log(col_two)
    // console.log(row_three)
    // console.log(row_four)
    // console.log(row_five)
    return ans
}

function num_to_binary(int) {
  x = int.toString(2)
  return x
}

function draw_outline(x, y, l) {
  ctx.strokeStyle = "#FF0000";
  // console.log(x,y)
  // console.log(x+l,y+l)
  ctx.strokeRect(x, y, x , y );

}
function draw_target(x, y, l) {
    ctx.font = length/7 + "px Arial";
    ctx.fillText("H", x*l, (y+1)*l);
}

function draw_number(x, y, l, num) {
  ctx.font = length/40 + "px Arial";
  ctx.fillText(num, (x*l) + l*.75, (y+1)*l - l*.8);
}




