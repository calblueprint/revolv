$(document).ready(function () {
    // method of drawing partial circles in d3 open source from http://jsfiddle.net/Wexcode/CrDUy/
    var radius = 100,
        padding = 10,
        radians = 2 * Math.PI;

    var dimension = (2 * radius) + (2 * padding),
        points = 50;

    var angle = d3.scale.linear()
        .domain([0, points-1])
        .range([0, radians]);

    var line = d3.svg.line.radial()
        .interpolate("basis")
        .tension(0)
        .radius(radius)
        .angle(function(d, i) { return angle(i); });

    var svg = d3.select("body").append("svg")
        .attr("width", dimension)
        .attr("height", dimension)
    .append("g");

    svg.append("path").datum(d3.range(points-24))
        .attr("class", "line")
        .attr("d", line)
        .attr("transform", "translate(" + (radius + padding) + ", " + (radius + padding) + ")");

});
