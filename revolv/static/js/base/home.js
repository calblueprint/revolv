$(document).ready(function () {
    // method of drawing partial circles in d3 open source from http://jsfiddle.net/Wexcode/CrDUy/
    var radius = 130,
        padding = 10;
        
    var dimension = (2 * radius) + (2 * padding);

    window.HOMEPAGE_PROJECT_DATA.forEach(function (data) {
        $(".project-badge.project-id-" + data.id).prepend("<svg>");
        var svg = d3.select(".project-badge.project-id-" + data.id + " svg")
            .attr("width", dimension)
            .attr("height", dimension)
        .append("g");

        var circleGrouping = svg.append("g").attr("class", "project-badge-circle-grouping");
        var partialGrouping = svg.append("g").attr("class", "project-badge-partial-grouping");

        drawD3PartialCircle(circleGrouping, ["project-badge-circle"], radius, padding, 1);
        var partialCompleteness = data.partialCompleteness;
        if (partialCompleteness <= 0.01 && partialCompleteness !== 0.0) partialCompleteness = 0.02;
        drawD3PartialCircle(partialGrouping, ["project-badge-line"], radius, padding, partialCompleteness);
    });

});
