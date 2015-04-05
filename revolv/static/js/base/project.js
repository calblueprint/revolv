$(document).ready(function () {
	var radius = 100,
        padding = 10;

    if ($(document).width() > 200 && $(document).width() < 800) {
        radius = 48;
    }

    // this line will get actual partial completeness
    var partialCompleteness = window.PARTIAL_COMPLETENESS;

    // use this for test purposes so you can see the progress bar
    var partialCompleteness = 0.7;

    var dimension = (2 * radius) + (2 * padding);

    var svg = d3.select(".internal-graphics-container")
        .attr("width", dimension)
        .attr("height", dimension)
        .append("g");

    var circleGrouping = svg.append("g").attr("class", "project-badge-circle-grouping");
    var partialGrouping = svg.append("g").attr("class", "project-badge-partial-grouping");

    drawD3PartialCircle(circleGrouping, ["project-badge-circle"], radius, padding, 1);

    drawD3PartialCircle(partialGrouping, ["project-badge-line"], radius, padding, partialCompleteness);
});
