$(document).ready(function () {
    draw();
});

$( window ).resize(function() {
    deleteCurrentCircles();
    draw();
});

var deleteCurrentCircles = function() {
    $(".dashboard-data-section-current .project-badge-circle-grouping").remove();
    $(".dashboard-data-section-current .project-badge-partial-grouping").remove();
    $(".dashboard-data-section-current .project-badge-circle").remove();
    $(".dashboard-data-section-current .project-badge-line" ).remove();
    $(".dashboard-data-section-current .outside-circle" ).remove();
};

/**
 * Resizes the text inside the speedometer.
 */
var setTextSize = function(radius) {

    var percentage_size = 3 * radius / 100;
    var repaid_size = percentage_size * 0.5;

    d3.selectAll(".percentage-text").attr("style", "font-size:" + percentage_size + "rem");
    d3.selectAll(".repaid").attr("font-size", "font-size:" + repaid_size + "rem");

};

/**
 * Resizes the iframe.
 */
var resizeIframe = function() {
    d3.select("iframe").attr("height", $(document).width() * 0.3 + "");
};

/**
 * Dynamically resizes text inside the speedometer, resizes the iframe, draws an outside circle, and draws an inner
 * partial circle based on the width of the existing screen.
 */
var draw = function() {
    var radius = $(document).width() * 0.12;
    setTextSize(radius);
    resizeIframe();

    var outsideCircle = d3.select(".dashboard-data-section-current .svg-graphics-container");
    // we have this check whether it is null because the currently selected project might not be completed
    if (!outsideCircle.empty()) {
        var outsideCircleRadius = 1.1 * radius;
        outsideCircle = outsideCircle.append("circle")
            .attr("class", "outside-circle")
            .attr("cx", "50%")
            .attr("cy", "50%")
            .attr("stroke", "#bbb")
            .attr("stroke-width", "3")
            .attr("fill", "white")
            .attr("r", outsideCircleRadius);
            // stroke="black" stroke-width="3"
            // .attr("r", radius + $(document).width() * 0.03 + "")
            // .attr("fill", "white");

        if (radius > 100 ){
            radius = 100;
            outsideCircleRadius = 1.1 * radius;
            outsideCircle.attr("r", outsideCircleRadius);
        }

        if (radius < 60 ) {
            radius = 60;
            outsideCircleRadius = 1.1 * radius;
            outsideCircle.attr("r", outsideCircleRadius);
        }
    }
    setTextSize(radius);
    var padding = radius * 0.1;

    // this line will get actual partial completeness - set this variable to something else if you want to test.
    var partialCompleteness = d3.select(".dashboard-data-section-current .percentage-container");
    if (!partialCompleteness.empty()) {
        partialCompleteness = parseFloat(partialCompleteness.text());
    } else {
        partialCompleteness = 0.0;
    }

    var dimension = (2 * radius) + (2 * padding);
    var translateVar = (radius + padding) * 0.5;

    var svg = d3.select(".dashboard-data-section-current .internal-graphics-container");
    // we have this check whether it is null because the currently selected project might not be completed
    if (!svg.empty()) {
        svg = svg.attr("width", dimension)
            .attr("height", dimension)
            .append("g");

        var stroke = radius * 0.2;
        var circleGrouping = svg.append("g").attr("class", "project-badge-circle-grouping").attr("stroke-width", stroke + "px");
        var partialGrouping = svg.append("g").attr("class", "project-badge-partial-grouping").attr("stroke-width", stroke + "px");

        drawD3PartialCircle(circleGrouping, ["project-badge-circle"], radius, padding, 1);
        drawD3PartialCircle(partialGrouping, ["project-badge-line"], radius, padding, partialCompleteness);
    }
};
