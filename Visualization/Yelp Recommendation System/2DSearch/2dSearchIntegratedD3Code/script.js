/**
 * Created by Justin on 4/19/2015.
 */
var csv_data;
var result;
var restaurantData;
var mapData = [];

var margin = 1;
var xFrame = 400;
var yFrame = 400;
var q;

var quads = {};
quads[0] = [[0, 0]];
quads[1] = [[0, 0]];
quads[2] = [[0, 0]];
quads[3] = [[0, 0]];

var sqrs = {};
sqrs[0] = [];
sqrs[1] = [];
sqrs[2] = [];
sqrs[3] = [];

var foodMap;

/*var tip = d3.tip().attr("class", "d3-tip").html(function(d) {
    return d.category + ': ' + d.name; });
*/
function generateMap(inputData) {
    var g = foodMap.selectAll("g").data(inputData).enter().append("svg:g")
        .attr("transform", function(d) {return "translate(" + d.x_axis + "," + d.y_axis + ")";})
        .attr("class", 'new')
        .style("opacity", 0);

    var rects = g.append("rect")
        .attr("width", function(d) {return d.size;})
        .attr("height", function(d) {return d.size;});

    var imgs = g.append("svg:image")
        .attr("width", function(d) {
            return d.size-2;
        })
        .attr("height", function(d) {
            return d.size-2;
        })
        .attr("xlink:href", function(d) {
            return d.src;
        })
        .attr("x",1)
        .attr("y",1)
        .attr("class", 'init');
        //.call(tip)
        //.on('mouseover', tip.show)
        //.on('mouseout', tip.hide);
//                    .append("svg:title")
//                    .text(function(d) { return d.name; });

    var transition = foodMap.transition().duration(750),
        delay = function(d, i) { return i * 100; };

    transition.selectAll("g")
        .delay(delay)
        .style("opacity", 0.8);

    setHover();
}

function setHover() {
    foodMap.selectAll("g").
        on("mouseover", function () {
            d3.select(this)
                .style("opacity", 1.0);
        })
        .on("mouseout", function () {
            d3.select(this)
                .style("opacity", 0.8);
        });
}

function getCoord(lenSquare, q, newCenter) {
    index = quads[q].getIdx(newCenter);
    quads[q].splice(index, 1);
    if (q == 0) {
        uX = newCenter[0] + margin;
        uY = newCenter[1] + margin + lenSquare;
        quads[q].push([newCenter[0] + lenSquare + 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] + lenSquare + 2 * margin]);
    } else if (q == 1) {
        uX = newCenter[0] + margin;
        uY = newCenter[1] - margin;
        quads[q].push([newCenter[0] + lenSquare + 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] - lenSquare - 2 * margin]);
    } else if (q == 2) {
        uX = newCenter[0] - lenSquare - margin;
        uY = newCenter[1] - margin;
        quads[q].push([newCenter[0] - lenSquare - 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] - lenSquare - 2 * margin]);
    } else if (q == 3) {
        uX = newCenter[0] - lenSquare - margin;
        uY = newCenter[1] + lenSquare + margin;
        quads[q].push([newCenter[0] - lenSquare - 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] + lenSquare + 2 * margin]);
    }
    sqrs[q].push([[uX, uY], [uX + lenSquare, uY - lenSquare]]);
}

var f = function (x, y) {
    return Math.pow(x, 2) + Math.pow(y, 2)
};

function optPoint() {
    var keys = Object.keys(quads);
    var tmp = Number.MAX_VALUE;
    keys.forEach(function (q) {
        quads[q].forEach(function (coord) {
            var x = coord[0],
                y = coord[1],
                dist = f(x, y);
            if (dist < tmp) {
                tmp = dist;
                result = ([q, [x, y], dist]);
            }
        });
    });
    return result;
}

function unpackSquare(thisSquare) {
    var d = {};
    d['lx'] = thisSquare[0][0];
    d['ly'] = thisSquare[0][1];
    d['rx'] = thisSquare[1][0];
    d['ry'] = thisSquare[1][1];
    return d
}

function checkOverlap(thisSquare, sqrs, q) {
    var d1 = unpackSquare(thisSquare);
    for (i in sqrs[q]) {
        var d2 = unpackSquare(sqrs[q][i]);
        if ((d1['lx'] > d2['rx'] || d2['lx'] > d1['rx']) || (d1['ly'] < d2['ry'] || d2['ly'] < d1['ry'])) {
        } else {
            return 0;
        }
    }
    return 1
}

Array.prototype.equals = function (array) {
    // if the other array is a falsy value, return
    if (!array)
        return false;

    // compare lengths - can save a lot of time
    if (this.length != array.length)
        return false;

    for (var i = 0, l = this.length; i < l; i++) {
        // Check if we have nested arrays
        if (this[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!this[i].equals(array[i]))
                return false;
        }
        else if (this[i] != array[i]) {
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;
        }
    }
    return true;
};

Array.prototype.getIdx = function (array) {
    for (var i = 0; i < this.length; i++) {
        if (this[i].equals(array)) {
            return i;
        }
    }
};

function getMaxOfArray(array) {
    return Math.max.apply(null, array);
}

function scaleData(array, maxV) {
    scaleFactor = 100 / maxV;
    for (i = 0; i < array.length; i++) {
        array[i] = array[i] * scaleFactor;
    }
    return array;
}

function output(sqrs, q) {
    res = [];
    for (q = 0; q < 4; q++) {
        for (i = 0; i < sqrs[q].length; i++) {
            d = unpackSquare(sqrs[q][i]);
            lenSquare = Math.abs(d['lx'] - d['rx']);
            var fX = d['lx'] + xFrame / 2;
            if (d['ly'] >= 0) {
                fY = yFrame / 2 - d['ly']
            } else {
                fY = yFrame / 2 + Math.abs(d['ly'])
            }
            res.push([fY, fX, lenSquare])
        }
    }

    res2 = [];
    tmp = {};
    for (s = 0; s < res.length; s++) {
        tmp["y_axis"] = res[s][0];
        tmp["x_axis"] = res[s][1];
        tmp["size"] = res[s][2];
        res2.push(tmp);
        tmp = {}
    }
    return res2
}

function main(data) {
    // get first four
    for (q = 0; q < 4; q++) {
        lenSquare = data.shift(); // pop first element
        getCoord(lenSquare, q, [0, 0])
    }

    //Hack for the fifth element
    lenSquare = data.shift();
    getCoord(lenSquare,3,quads[3][1]);

    // remaining squares
    for (i = 0; i < data.length; i++) {
        lenSquare = data[i];// pop first element
        optData = optPoint(quads);
        getCoord(lenSquare, optData[0], optData[1])
    }

    return output(sqrs, q)
}

function createData(selectedValue) {
//    var selectedValue = d3.event.target.value;
    foodMap.selectAll("g").remove();
    restaurantData = csv_data.filter(function (d) {
        return d.restaurant == selectedValue
    });
    restaurantData.sort(function (a, b) {
        return b.review_num - a.review_num
    });
    restaurantData = restaurantData.slice(0, 14);
    input_data = [];
    restaurantData.forEach(function (d) {
        input_data.push(Math.sqrt(+d.review_num))
    });
    var maxV = getMaxOfArray(input_data);
    input_data = scaleData(input_data, maxV);
    q = 0;
    quads[0] = [[0, 0]];
    quads[1] = [[0, 0]];
    quads[2] = [[0, 0]];
    quads[3] = [[0, 0]];
    sqrs[0] = [];
    sqrs[1] = [];
    sqrs[2] = [];
    sqrs[3] = [];
    result = main(input_data);

    result = result.sort(function (a, b) {
        return b.size - a.size;
    });

    mapData = [];

    for (i = 0; i < restaurantData.length; i++) {
        var tmp = {};
        for (key in restaurantData[i]) {
            tmp[key] = restaurantData[i][key];
        }
        for (key in result[i]) {
            tmp[key] = result[i][key];
        }
        mapData.push(tmp)
    }

    generateMap(mapData);
}


d3.csv("foodMap.csv", function (data) {
    data.forEach(function (d) {
        d.foodkey = +d.foodkey;
        d.src = d.src;
        d.business_id = d.business_id;
        d.name = d.name;
        d.review_num = +d.review_num;
        d.description = d.description;
        d.prices = d.prices;
        d.restaurant = d.restaurant
    });
    foodMap = d3.select("#foodMap").append("svg").attr("width", xFrame).attr("height", yFrame);
    csv_data = data;

    var dropDown = d3.select("#table_container").append("select")
        .attr("name", "restaurant-list");

    var options = dropDown.selectAll("option")
        .data(d3.map(data, function (d) {
            return d.restaurant;
        }).keys().sort())
        .enter()
        .append("option");

    options.text(function (d) {
        return d;
    })
        .attr("value", function (d) {
            return d;
        });



    restaurantData = data;
    restaurantData.sort(function (a, b) {
        return b.review_num - a.review_num
    });
    restaurantData = restaurantData.slice(0, 14);
    input_data = [];
    restaurantData.forEach(function (d) {
        input_data.push(Math.sqrt(+d.review_num))
    });
    var maxV = getMaxOfArray(input_data);
    input_data = scaleData(input_data, maxV);
    result = main(input_data);

    result = result.sort(function (a, b) {
        return b.size - a.size;
    });

    mapData = [];

    for (i = 0; i < restaurantData.length; i++) {
        var tmp = {};
        for (key in restaurantData[i]) {
            tmp[key] = restaurantData[i][key];
        }
        for (key in result[i]) {
            tmp[key] = result[i][key];
        }
        mapData.push(tmp)
    }

    generateMap(mapData);

    d3.select("#table_container").on("change", createData);

});