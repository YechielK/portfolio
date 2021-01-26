function download() {
    var download = document.getElementById("download");
    var image = document.getElementById("myCanvas").toDataURL("image/png")
        .replace("image/png", "image/octet-stream");
    download.setAttribute("href", image);
    }

function draw_line(x, y, length, name, val, ctx, a, b) {

    width = length*1.44

    if (name == 'a^b') {
        x_start = x
        y_start = y
        x_end = x - (length/10)
        y_end = y- (length/10)
        x_txt = x - (length/5)
        prob = "P(" + b + "^" + a + ")";
    }

    if (name == 'b`^a') {
        x_start = x
        y_start = y + length
        x_end = x - (length/10)
        y_end = y + length + (length/10)
        x_txt = x - (length/5)
        prob = "P(" + b + "`^" + a + ")";
    }
    
    if (name == 'b^a`') {
        x_start = x + length
        y_start = y
        x_end = x + length + (length/10)
        y_end = y- (length/10)
        x_txt = x + length + (length/10)
        prob = "P(" + b + "^" + a + "`)";
    }

    if (name == 'a`^b`') {
        x_start = x + length
        y_start = y + length
        x_end = x + length + (length/10)
        y_end = y + length + (length/10)
        x_txt = x + length + (length/10)
        prob = "P(" + b + "`^" + a + "`)";
    }

    // draw line
    ctx.beginPath();
    ctx.moveTo(x_start, y_start);
    ctx.lineTo(x_end,y_end);
    ctx.stroke();

    ctx.font = width/48  + "px Arial";

    // draw prob name
    ctx.fillText(prob, x_txt, y_end);

    //draw prob val
    ctx.fillText(val, x_txt , y_end + width/36);
}

function draw_triangle(x, y, length, name, val, ctx, a, b) {
    
    width = length*1.44
    
    if (name == 'b|a`') {
        x_hi_start = x + length
        y_hi_start = y 
        x_lo_start = x + length
        y_lo_start = y + (length * val)
        x_end = x + length + (length/10)
        y_end = y + (length * val)/2
        x_txt =  x + length + (length/10)
        prob = "P(" + b + "|" + a + "`)";
    }

    if (name == 'b`|a`') {
        x_hi_start = x + length
        y_hi_start = y +( length * (1 -val))
        x_lo_start = x + length
        y_lo_start = y +  length
        x_end = x + length + (length/10)
        y_end = y + (length * ((1-val) + val/2))
        x_txt =  x + length + (length/10)
        prob = "P(" + b + "`|" + a + "`)";
    }

    if (name == 'b|a') {
        x_hi_start = x
        y_hi_start = y
        x_lo_start = x 
        y_lo_start = y + (length *val)
        x_end = x - (length/10)
        y_end = y+ (length * val)/2;
        x_txt =  x - (length/5)
        prob = "P(" + b + "|" + a + ")";
    }

    if (name == 'b`|a') {
        x_hi_start = x
        y_hi_start = y + (length * (1-val))
        x_lo_start = x 
        y_lo_start = y + length
        x_end = x - (length)/10
        y_end = y + (length * ((1-val) + val/2))
        x_txt =  x - (length/5)
        prob = "P(" + b + "`|" + a + ")";
    }

    if (name == 'a') {
        x_hi_start = x
        y_hi_start = y
        x_lo_start = x + (length * val)
        y_lo_start = y 
        x_end = x + (length *val)/2
        y_end = y- (length/10)
        x_txt =  x + (length * val)/2 
        prob = "P(" + a + ")" ;
    }

    if (name == 'a`') {
        x_hi_start = x + (length * (1-val))
        y_hi_start = y
        x_lo_start = x + length
        y_lo_start = y 
        x_end = x + (length * (1-val))/2 + (length)/2
        y_end = y - (length/10)
        x_txt =  x + (length * (1-val))/2 + (length)/2
        prob = "P(" + a + "`)" ;
    }

    // top line
    ctx.beginPath();
    ctx.moveTo(x_hi_start, y_hi_start);
    ctx.lineTo(x_end, y_end);
    ctx.stroke();

    // bottom line
    ctx.beginPath();
    ctx.moveTo(x_lo_start, y_lo_start);
    ctx.lineTo(x_end, y_end);
    ctx.stroke();

    ctx.font = width/48  + "px Arial";

    // probability
    ctx.fillText(prob, x_txt, y_end);
    
    // val
    ctx.fillText(val, x_txt, y_end + width/36);
}

function draw_square(v, a, b) {
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);

    length = c.width / 1.44
    m = 10
    x = length/5
    y = length/5
    origin = 0
    circle_size = .2

    ctx.beginPath();
    ctx.rect(x, y, length, length);
    ctx.stroke();

    var givens = ['a', 'a`', 'b|a`', 'b`|a`', 'b|a', 'b`|a']
    var ands = ['a^b', 'b`^a', 'b^a`', 'a`^b`']

    // P(A) and P(A`)
    ctx.beginPath();
    ctx.moveTo(x + (length * v['a']), y);
    ctx.lineTo(x + (length * v['a']), y + length);
    ctx.stroke();

    // P(B|A) and P(B`|A)
    ctx.beginPath();
    ctx.moveTo(x, y + (length *  v['b|a'] ));
    ctx.lineTo(x + (length * v['a']), y +  (length * v['b|a']));
    ctx.stroke();

    // P(B|A`) and P(B`|A`)
    ctx.beginPath();
    ctx.moveTo(x + (length * v['a'] ), y + (length * v['b|a`'] ));
    ctx.lineTo(x + length, y +  (length * v['b|a`'] ));
    ctx.stroke();

    for (let i = 0; i < givens.length; i++) {
        draw_triangle(x, y, length, givens[i], v[givens[i]] , ctx, a, b)   
    }

    for (let i = 0; i < ands.length; i++) {
        draw_line(x, y, length, ands[i], v[ands[i]], ctx, a, b)
    }

    // TODO
    // Fix ration of amount of circles so lines that cut through are
    //circles
    // for (let i = x + length/(2 * m); i <x + length; i+=length/(1 * m)) {
    //     for (let j = y + length/(2 * m); j <y + length; j+=length/(1 * m)) {
    //         ctx.beginPath();
    //         ctx.arc(j, i, length/(2 * m) * circle_size, 0, 2 * Math.PI);
    //         ctx.stroke();
    //     }
    // }
}




