/**
 * Created by Justin on 4/19/2015.
 */
var csv_data;
var result;
var restaurantData;
var mapData = [];

var lenMargin = 1;
var xFrame = 300;
var yFrame = 300;
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

var tip = d3.tip().attr("class", "d3-tip").html(function(d) {
    return "<p>" + d.review_num + " Reviews</p>" +
        "<p><span>" +
        d.name +
        "</span></p>" +
        "<p><i>" +
        d.description +
        "</i></p>"; });

//        "<div class=""description""><p>" +
//        d.description; });

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
        .attr("class", 'init')
        .call(tip)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
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
        uX = newCenter[0] + lenMargin;
        uY = newCenter[1] + lenMargin + lenSquare;
        quads[q].push([newCenter[0] + lenSquare + 2 * lenMargin, newCenter[1]], [newCenter[0], newCenter[1] + lenSquare + 2 * lenMargin]);
    } else if (q == 1) {
        uX = newCenter[0] + lenMargin;
        uY = newCenter[1] - lenMargin;
        quads[q].push([newCenter[0] + lenSquare + 2 * lenMargin, newCenter[1]], [newCenter[0], newCenter[1] - lenSquare - 2 * lenMargin]);
    } else if (q == 2) {
        uX = newCenter[0] - lenSquare - lenMargin;
        uY = newCenter[1] - lenMargin;
        quads[q].push([newCenter[0] - lenSquare - 2 * lenMargin, newCenter[1]], [newCenter[0], newCenter[1] - lenSquare - 2 * lenMargin]);
    } else if (q == 3) {
        uX = newCenter[0] - lenSquare - lenMargin;
        uY = newCenter[1] + lenSquare + lenMargin;
        quads[q].push([newCenter[0] - lenSquare - 2 * lenMargin, newCenter[1]], [newCenter[0], newCenter[1] + lenSquare + 2 * lenMargin]);
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

function optPoint2(lenSquare){
    var keys = Object.keys(quads);
    var tmp = [];
    var procData = keys.forEach(function(q) {
        quads[q].forEach(function(pt) {
            var dist = f(pt[0],pt[1]);
            tmp.push([q, pt, dist])
        });
    });
    sortedTmp = tmp.sort(function(a,b) {return a[2] - b[2]});
    for (i=0; i<sortedTmp.length;i++) {
        q = sortedTmp[i][0];
        thisPt = sortedTmp[i][1];
        if (q == 0) {
            var uX = thisPt[0] + lenMargin;
            var uY = thisPt[1] + lenMargin + lenSquare
        } else if (q == 1) {
            var uX = thisPt[0] + lenMargin;
            var uY = thisPt[1] - lenMargin
        } else if (q == 2) {
            var uX = thisPt[0] - lenSquare - lenMargin;
            var uY = thisPt[1] - lenMargin
        } else if (q == 3) {
            var uX = thisPt[0] - lenSquare - lenMargin;
            var uY = thisPt[1] + lenSquare + lenMargin
        }
        var thisSquare = [[uX,uY],[uX+lenSquare,uY-lenSquare]];
        if (checkOverlap(thisSquare, sqrs, q) == 1) {
            return sortedTmp[i]
        }
    }
    return -1
}

function unpackSquare(thisSquare) {
    var d = {};
    d['lx'] = thisSquare[0][0];
    d['ly'] = thisSquare[0][1];
    d['rx'] = thisSquare[1][0];
    d['ry'] = thisSquare[1][1];
    return d
}

function checkOverlap(thisSquare, sqrs, q){
    var d1 = unpackSquare(thisSquare);
    var sQuad = sqrs[q];
    for (j=0; j<sQuad.length;j++) {
        var d2 = unpackSquare(sQuad[j]);
        if ((d1['lx']>d2['rx'] || d2['lx']>d1['rx']) || (d1['ly']<d2['ry'] || d2['ly']<d1['ry'])){
            continue;
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
    scaleFactor = 110 / maxV;
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

    if (data.length == 1) {
        uX = -data[0]/2 + xFrame/2;
        uY = yFrame/2 - data[0]/2;
        res = [{'y_axis': uY, 'x_axis': uX, 'size': data[0]}];
        return res
    } else if (data.length == 2) {
        res = [];
        uX = -data[0]/2 + xFrame/2;
        uY = yFrame/2 - data[0];
        res.push({'y_axis': uY, 'x_axis': uX, 'size': data[0]});
        uX = -data[1]/2 + xFrame/2;
        uY = yFrame/2;
        res.push({'y_axis': uY, 'x_axis': uX, 'size': data[1]});
        return res
    } else {
        for (q = 0; q < 4; q++) {
            lenSquare = data.shift(); // pop first element
            getCoord(lenSquare, q, [0, 0])
        }

        //Hack for the fifth element
        lenSquare = data.shift();
        getCoord(lenSquare,3,quads[3][1]);

        // remaining squares
        for (k=0; k<data.length; k++) {
            var lenSquare = data[k]; // pop first element
            var optData = optPoint2(lenSquare);
            if (optData == -1) {
            } else {
                getCoord(lenSquare, optData[0], optData[1])
            }
        }
        return output(sqrs, q)
    }
    // get first four

}

            // This recieves messages of type "testmessage" from the server.
Shiny.addCustomMessageHandler("FoodMap",
  function(message) {
                var restName = JSON.stringify(message)
                //var objJSON = eval(selectedValue);
                //var restName = objJSON.restname;
                var i = restName.indexOf('.');
                var formRestName = restName.substring(i+2,restName.length - 2);
                createData(formRestName);
   
  	           
                //alert(JSON.stringify(message));
  }
);

function createData(selectedValue) {
    
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


    

    d3.select("#table_container").on("change", createData);

});
