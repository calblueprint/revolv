$(document).ready(function () {
    draw();
});

$( window ).resize(function() {
    $(".project-badge-circle-grouping").remove();
    $(".project-badge-partial-grouping").remove();
    $(".project-badge-circle").remove();
    $(".project-badge-line" ).remove();
    $(".outside-circle" ).remove();
    draw();
});

/**
 * Resizes the text inside the speedometer.
 */
var setTextSize = function(radius) {

    var percentage_size = 3 * radius / 100;
    var funded_size = percentage_size * 0.5;

    d3.select(".percentage-text").attr("style", "font-size:" + percentage_size + "rem");
    d3.select(".funded").attr("font-size", "font-size:" + funded_size + "rem");

};

/**
 * Resizes the iframe.
 */
var resizeIframe = function() {
    d3.select("iframe").attr("height", $(document).width() * 0.38 + "");

    if ($(document).width() < 500) {
        d3.select("iframe").attr("height", $(document).width() * 0.45 + "");
    }
};

/**
 * Dynamically resizes text inside the speedometer, resizes the iframe, draws an outside circle, and draws an inner
 * partial circle based on the width of the existing screen.
 */
var draw = function() {

    var radius = $(document).width() * 0.12;
    setTextSize(radius);

    resizeIframe();

    var outsideCircle = d3.select(".svg-graphics-container")
        .append("circle")
        .attr("class", "outside-circle")
        .attr("cx", "50%")
        .attr("cy", "50%")
        .attr("r", radius + $(document).width() * 0.03 + "")
        .attr("fill", "white");

    if (radius > 100 ){
        radius = 100;
        outsideCircle.attr("r", 125);
    }

    if (radius < 60 ) {
        radius = 60;
        outsideCircle.attr("r", 75);
    }

    setTextSize(radius);
    var padding = radius * 0.1;

    // this line will get actual partial completeness - set this variable to something else if you want to test.
    var partialCompleteness = window.PARTIAL_COMPLETENESS;

    var dimension = (2 * radius) + (2 * padding);
    var translateVar = (radius + padding) * 0.5;

    var svg = d3.select(".internal-graphics-container")
        .attr("width", dimension)
        .attr("height", dimension)
        .append("g");

    var stroke = radius * 0.2;
    var circleGrouping = svg.append("g").attr("class", "project-badge-circle-grouping").attr("stroke-width", stroke + "px");
    var partialGrouping = svg.append("g").attr("class", "project-badge-partial-grouping").attr("stroke-width", stroke + "px");

    drawD3PartialCircle(circleGrouping, ["project-badge-circle"], radius, padding, 1);
    drawD3PartialCircle(partialGrouping, ["project-badge-line"], radius, padding, partialCompleteness);
};
