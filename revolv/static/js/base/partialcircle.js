/**
 * Draws a partial circle.
 * @param {string} title - The destination class name that the circle should be drawn to
 * @param {string[]} classes - An array of classes that should be added to the created object.
 * @param {number} radius - The radius of this circle.
 * @param {number} padding - The padding of this circle.
 * @param {number} partial - The partial completeness of this circle, as a float from 0 to 1.
 */
var drawD3PartialCircle = function (destination, classes, radius, padding, partial) {
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