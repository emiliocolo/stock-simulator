circleRadii = [40, 20, 10]

var svgContainer = d3.select("#circles").append("svg")
                                    .attr("width", 800)
                                    .attr("height", 100)
                                    .style("border", "1px solid red");

var circles = svgContainer.selectAll("circle")
                        .data(circleRadii)
                        .enter()
                        .append("circle")

var circleAttributes = circles
                       .attr("cx", 50)
                       .attr("cy", 50)
                       .attr("r", function (d) { return d; })
                       .style("fill", function(d) {
                                var returnColor;
                                        if (d === 40) { returnColor = "green";
                                        } else if (d === 20) { returnColor = "purple";
                                        } else if (d === 10) { returnColor = "red"; }
                                        return returnColor;
                                });

var spaceCircles = [30, 70, 110];

var svgContainer = d3.select("#circles").append("svg")
                                    .attr("width", 200)
                                    .attr("height", 100)
                                    .style("border", "1px solid blue");

var circles = svgContainer.selectAll("circle")
                          .data(spaceCircles)
                          .enter()
                          .append("circle");

var circleAttributes = circles
                       .attr("cx", function (d) { return d; })
                       .attr("cy", function (d) { return 50; })
                       .attr("r", 20 )
                       .style("fill", function(d) {
                            var returnColor;
                            if (d === 30) { returnColor = "green";
                            } else if (d === 70) { returnColor = "purple";
                            } else if (d === 110) { returnColor = "red"; }
                            return returnColor;
                       });

var jsonCircles = [
    {
    "x_axis": 30,
    "y_axis": 30,
    "radius": 20,
    "color" : "green"
    }, {
    "x_axis": 70,
    "y_axis": 70,
    "radius": 20,
    "color" : "purple"
    }, {
    "x_axis": 110,
    "y_axis": 100,
    "radius": 20,
    "color" : "red"
}];


var svgContainer = d3.select("#circles").append("svg")
                        .attr("width", 200)
                        .attr("height", 200)
                        .style("border", "1px solid white");

var circles = svgContainer.selectAll("circle")
                        .data(jsonCircles)
                        .enter()
                        .append("circle");

var circleAttributes = circles
                        .attr("cx", function (d) { return d.x_axis; })
                        .attr("cy", function (d) { return d.y_axis; })
                        .attr("r", function (d) { return d.radius; })
                        .style("fill", function(d) { return d.color; });