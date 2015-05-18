// Code goes here
        var csv_data;
        var res;
        var restaurantData;
        var brahd = [];
        var brah;

        d3.csv("vizdata.csv", function (data) {
            data.forEach(function (d) {
                d.foodkey = +d.foodkey;
                d.src = d.src; // convert "Year" column to Date
                d.business_id = d.business_id;
                d.name = d.name;
                d.review_num = +d.review_num;
                d.description = d.description;
                d.prices = d.prices;
                d.restaurant = d.restaurant
            });

            csv_data = data;

            /*var dropDown = d3.select("#table_container").append("select")
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
                    });*/

            function getCoord(Lbrah, q, newCenter) {
                index = quads[q].getIdx[newCenter];
                quads[q].splice(index, 1);
                if (q == 0) {
                    var uX = newCenter[0] + margin;
                    var uY = newCenter[1] + margin + Lbrah;
                    quads[q].push([newCenter[0] + Lbrah + 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] + Lbrah + 2 * margin]);
                } else if (q == 1) {
                    var uX = newCenter[0] + margin;
                    var uY = newCenter[1] - margin;
                    quads[q].push([newCenter[0] + Lbrah + 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] - Lbrah - 2 * margin]);
                } else if (q == 2) {
                    var uX = newCenter[0] - Lbrah - margin;
                    var uY = newCenter[1] - margin;
                    quads[q].push([newCenter[0] - Lbrah - 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] - Lbrah - 2 * margin]);
                } else if (q == 3) {
                    var uX = newCenter[0] - Lbrah - margin;
                    var uY = newCenter[1] + Lbrah + margin;
                    quads[q].push([newCenter[0] - Lbrah - 2 * margin, newCenter[1]], [newCenter[0], newCenter[1] + Lbrah + 2 * margin]);
                }
                sqrs[q].push([[uX, uY], [uX + Lbrah, uY - Lbrah]]);
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
                            res = ([q, [x, y], dist]);
                        }
                    });
                });
                return res;
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
                        break;
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
                        Lbrah = Math.abs(d['lx'] - d['rx']);
                        var fX = d['lx'] + xFrame / 2;
                        if (d['ly'] >= 0) {
                            var fY = yFrame / 2 - d['ly']
                        } else {
                            var fY = yFrame / 2 + Math.abs(d['ly'])
                        }
                        res.push([fY, fX, Lbrah])
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
                    Lbrah = data.shift(); // pop first element
                    getCoord(Lbrah, q, [0, 0])
                }

                // remaining squares
                for (i = 0; i < data.length; i++) {
                    Lbrah = data[i];// pop first element
                    optData = optPoint(quads);
                    getCoord(Lbrah, optData[0], optData[1])
                }

                return output(sqrs, q)
            }

            function setHover() {
                treemap.selectAll("g").
                        on("mouseover", function () {
                            d3.select(this)
                                    .style("opacity", 1.0);
                        })
                        .on("mouseout", function () {
                            d3.select(this)
                                    .style("opacity", 0.7);
                        });
            }

            var margin = 1;
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

            var width = 300;
            var height = 300;

            var treemap = d3.select("#treemap2").append("svg").attr("width", width).attr("height", height);

            function createData() {
                var selectedValue = d3.event.target.value;
                d3.selectAll("g").remove();
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
                res = main(input_data);

                brah = res.sort(function (a, b) {
                    return b.size - a.size;
                });

                brahd = [];

                for (i = 0; i < restaurantData.length; i++) {
                    var tmp = {};
                    for (var key in restaurantData[i]) {
                        tmp[key] = restaurantData[i][key];
                    }
                    for (var key in brah[i]) {
                        tmp[key] = brah[i][key];
                    }
                    brahd.push(tmp)
                }


//                var g = treemap.selectAll("g").data(res).enter().append("svg:g")
//                        .attr("transform", function (d) {
//                            return "translate(" + d.x_axis + "," + d.y_axis + ")";
//                        })
//                        .attr("class", 'new')
//                        .style("opacity", 0);
//
//                var rects = g.append("rect")
//                        .attr("width", function (d) {
//                            return d.size;
//                        })
//                        .attr("height", function (d) {
//                            return d.size;
//                        });
//
//                var transition = treemap.transition().duration(750),
//                        delay = function (d, i) {
//                            return i * 100;
//                        };
//
//                transition.selectAll("g")
//                        .delay(delay)
//                        .style("opacity", 0.5);


                var g = treemap.selectAll("g").data(brahd).enter().append("svg:g")
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
                        .append("svg:title")
                        .text(function(d) { return d.name; });

                var transition = treemap.transition().duration(750),
                        delay = function(d, i) { return i * 100; };

                transition.selectAll("g")
                        .delay(delay)
                        .style("opacity", 0.7);

                setHover();
            }
            
            // This recieves messages of type "testmessage" from the server.
Shiny.addCustomMessageHandler("FoodMap",
  function(message) {
                var restName = JSON.stringify(message)
                //var objJSON = eval(selectedValue);
                //var restName = objJSON.restname;
                var i = restName.indexOf('.');
                var formRestName = restName.substring(i+2,restName.length - 2);
                shinyEvent(formRestName);
   
  	           
                //alert(JSON.stringify(message));
  }
);
            
            
            function shinyEvent(selectedValue) {
                
		//alert(selectedValue) ;
                treemap.selectAll("g").remove();
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
                res = main(input_data);

                brah = res.sort(function (a, b) {
                    return b.size - a.size;
                });

                brahd = [];

                for (i = 0; i < restaurantData.length; i++) {
                    var tmp = {};
                    for (var key in restaurantData[i]) {
                        tmp[key] = restaurantData[i][key];
                    }
                    for (var key in brah[i]) {
                        tmp[key] = brah[i][key];
                    }
                    brahd.push(tmp)
                }


                var g = treemap.selectAll("g").data(brahd).enter().append("svg:g")
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
                        .append("svg:title")
                        .text(function(d) { return d.name; });

                var transition = treemap.transition().duration(750),
                        delay = function(d, i) { return i * 100; };

                transition.selectAll("g")
                        .delay(delay)
                        .style("opacity", 0.7);

                setHover();
            }

            d3.select("#table_container").on("change", createData);

        });


