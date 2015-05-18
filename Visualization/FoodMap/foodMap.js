/**
 * Created by Justin on 4/19/2015.
 */
var csv_data;
var result;
var restaurantData;
var mapData = [];

var scaling = 180;
var lenMargin = 1;
var xFrame = 800;
var yFrame = 800;
var q;

var quads = {};
var sqrs = {};

var foodMap;

// Using d3-tip to generate tooltips
var tip = d3.tip().attr("class", "d3-tip").html(function (d) {
    return "<p>" + d.review_num + " Reviews</p>" +
        "<p><span>" +
        d.name +
        "</span></p>" +
        "<p><i>" +
        d.description +
        "</i></p>";
});

// Generating all the elements and transition of the d3 food map
function generateMap(inputData) {
    var g = foodMap.selectAll("g").data(inputData).enter().append("svg:g")
        .attr("transform", function (d) {
            return "translate(" + d.x_axis + "," + d.y_axis + ")";
        })
        .attr("class", 'new')
        .style("opacity", 0);

    g.append("rect")
        .attr("width", function (d) {
            return d.size;
        })
        .attr("height", function (d) {
            return d.size;
        });

    g.append("svg:image")
        .attr("width", function (d) {
            return d.size - 2;
        })
        .attr("height", function (d) {
            return d.size - 2;
        })
        .attr("xlink:href", function (d) {
            return d.src;
        })
        .attr("x", 1)
        .attr("y", 1)
        .attr("class", 'init')
        .call(tip); // d3-tip needs to be called here instead of after transition to prevent errors

    var transition = foodMap.transition().duration(750),
        delay = function (d, i) {
            return i * 100;
        };

    transition.selectAll("g")
        .delay(delay)
        .style("opacity", 0.8)
        .each("end",function () {
            d3.select(this).on("mouseover", function () {
                d3.select(this)
                    .style("opacity", 1.0);
            })
                .on("mouseout", function () {
                    d3.select(this)
                        .style("opacity", 0.8);
                })
                //.call(tip)
                .on('mouseover', tip.show)
                .on('mouseout', tip.hide);
        });

}

// List of functions to calculate sizing and coordinates
var f = function (x, y) {
    return Math.pow(x, 2) + Math.pow(y, 2)
};


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
    var sQuad = sqrs[q];
    for (j = 0; j < sQuad.length; j++) {
        var d2 = unpackSquare(sQuad[j]);
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
    scaleFactor = scaling / maxV;
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

    function optPoint2(lenSquare) {
        var keys = Object.keys(quads);
        var tmp = [];
        var procData = keys.forEach(function (q) {
            quads[q].forEach(function (pt) {
                var dist = f(pt[0], pt[1]);
                tmp.push([q, pt, dist])
            });
        });
        sortedTmp = tmp.sort(function (a, b) {
            return a[2] - b[2]
        });
        for (i = 0; i < sortedTmp.length; i++) {
            q = sortedTmp[i][0];
            thisPt = sortedTmp[i][1];
            if (q == 0) {
                uX = thisPt[0] + lenMargin;
                uY = thisPt[1] + lenMargin + lenSquare
            } else if (q == 1) {
                uX = thisPt[0] + lenMargin;
                uY = thisPt[1] - lenMargin
            } else if (q == 2) {
                uX = thisPt[0] - lenSquare - lenMargin;
                uY = thisPt[1] - lenMargin
            } else if (q == 3) {
                uX = thisPt[0] - lenSquare - lenMargin;
                uY = thisPt[1] + lenSquare + lenMargin
            }
            var thisSquare = [[uX, uY], [uX + lenSquare, uY - lenSquare]];
            if (checkOverlap(thisSquare, sqrs, q) == 1) {
                return sortedTmp[i]
            }
        }
        return -1
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

    q = 0;
    quads[0] = [[0, 0]];
    quads[1] = [[0, 0]];
    quads[2] = [[0, 0]];
    quads[3] = [[0, 0]];
    sqrs[0] = [];
    sqrs[1] = [];
    sqrs[2] = [];
    sqrs[3] = [];

    if (data.length == 1) {
        uX = -data[0] / 2 + xFrame / 2;
        uY = yFrame / 2 - data[0] / 2;
        res = [{'y_axis': uY, 'x_axis': uX, 'size': data[0]}];
        return res
    } else if (data.length == 2) {
        res = [];
        uX = -data[0] / 2 + xFrame / 2;
        uY = yFrame / 2 - data[0] - lenMargin;
        res.push({'y_axis': uY, 'x_axis': uX, 'size': data[0]});
        uX = -data[1] / 2 + xFrame / 2;
        uY = yFrame / 2 + lenMargin;
        res.push({'y_axis': uY, 'x_axis': uX, 'size': data[1]});
        return res
    } else {
        for (q = 0; q < 4; q++) {
            lenSquare = data.shift(); // pop first element
            getCoord(lenSquare, q, [0, 0])
        }

        //Hack for the fifth element
        lenSquare = data.shift();
        getCoord(lenSquare, 3, quads[3][1]);

        // remaining squares
        for (k = 0; k < data.length; k++) {
            var lenSquare = data[k]; // pop first element
            var optData = optPoint2(lenSquare);
            if (optData == -1) {
            } else {
                getCoord(lenSquare, optData[0], optData[1])
            }
        }
        return output(sqrs, q)
    }

}

// Function call to filter and generate data
function createData() {
    var selectedValue = d3.event.target.value;
    foodMap.selectAll("g").remove();
    restaurantData = csv_data.filter(function (d) {
        return d.restaurant == selectedValue;
    });
    restaurantData.sort(function (a, b) {
        return b.review_num - a.review_num;
    });
    restaurantData = restaurantData.slice(0, 25);
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
        for (itm in restaurantData[i]) {
            tmp[itm] = restaurantData[i][itm];
        }
        for (itm in result[i]) {
            tmp[itm] = result[i][itm];
        }
        mapData.push(tmp)
    }

    generateMap(mapData);
}

// Loading data
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

    // Still can't figure out why the svg generation needs to be here
    foodMap = d3.select("#foodMap").append("svg").attr("width", xFrame).attr("height", yFrame);

    csv_data = data;

    // Generating the initial map
    function initMap() {
        restaurantData = data;
        restaurantData.sort(function (a, b) {
            return b.review_num - a.review_num
        });
        restaurantData = restaurantData.slice(0, 25);
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
            for (itm in restaurantData[i]) {
                tmp[itm] = restaurantData[i][itm];
            }
            for (itm in result[i]) {
                tmp[itm] = result[i][itm];
            }
            mapData.push(tmp)
        }

        generateMap(mapData);
    }

    initMap();

    // Generating the dropdown
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

    // Event listener for the dropdown menu
    d3.select("#table_container").on("change", createData);

});