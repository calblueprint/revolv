var drawD3PartialTriangle = function (destination, classes, radius, padding, partial) {
    var points = 100,
        pointsToDraw = Math.floor(points * partial),
        radians = 2 * Math.PI;

    var angle = d3.scale.linear()
        .domain([0, points-1])
        .range([0, radians]);

    var line = d3.svg.line.radial()
        .interpolate("basis")
        .tension(0)
        .radius(radius)
        .angle(function(d, i) { return -angle(i); });

    var result = destination.append("path").datum(d3.range(pointsToDraw));

    classes.forEach(function (cls) {
        var currentClass = result.attr("class");
        if (currentClass) {
            result.attr("class", currentClass + " " + cls);
        } else {
            result.attr("class", cls);
        }
    });

    result.attr("d", line)
        .attr("transform", "translate(" + (radius + padding) + ", " + (radius + padding) + ")");
};

$(document).ready(function () {
    // method of drawing partial circles in d3 open source from http://jsfiddle.net/Wexcode/CrDUy/
    var radius = 130,
        padding = 10,
        radians = 2 * Math.PI;

    var dimension = (2 * radius) + (2 * padding);

    window.HOMEPAGE_PROJECT_DATA.forEach(function (data) {
        var svg = d3.select(".project-badge.project-id-" + data.id).append("svg")
            .attr("width", dimension)
            .attr("height", dimension)
        .append("g");

        var circleGrouping = svg.append("g").attr("class", "project-badge-circle-grouping");
        var partialGrouping = svg.append("g").attr("class", "project-badge-partial-grouping");

        drawD3PartialTriangle(circleGrouping, ["project-badge-circle"], radius, padding, 1);
        var partialCompleteness = data.partialCompleteness;
        if (partialCompleteness <= 0.01) partialCompleteness = 0.02;
        drawD3PartialTriangle(partialGrouping, ["project-badge-line"], radius, padding, partialCompleteness);
    });

});
