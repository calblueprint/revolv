

/**
 * Resizes the text inside the speedometer.
 */
var setTextSize = function(radius) {

    var percentage_size = 3 * radius / 100;
    var funded_size = percentage_size * 0.5;

  //Select All projects and set there "% funded" font size
    d3.selectAll(".percentage-text").attr("style", "font-size:" + percentage_size + "rem");
    d3.selectAll(".funded").attr("font-size", "font-size:" + funded_size + "rem");

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
 * This function is copied from previous project.js and moved here as a common utility
 * This function draws an outside circle, and draws an inner partial circle based on the given radius and radiusRatio
 * @param radius
 * @param radiusRatio higher the radiusRation lesser is the radius, ratioRatio comes into picture when there are multiple
 * active projects. Otherwise the behaviour remains same.
 */
var drawCircle = function(radius,radiusRatio){
    var outsideCircles = d3.selectAll(".svg-graphics-container");
    outsideCircles =outsideCircles.append("circle")
        .attr("class", "outside-circle")
        .attr("cx", "50%")
        .attr("cy", "50%")
        .attr("r", radius + $(document).width() * 0.03 + "")
        .attr("fill", "white");


    if (radius > 100/radiusRatio){
        radius = 100/radiusRatio;
        outsideCircles.attr("r", 125/radiusRatio);
    }

    if (radius < 60/radiusRatio ) {
        radius = 60/radiusRatio;
        outsideCircles.attr("r", 75/radiusRatio);
    }

    setTextSize(radius);
    var padding = radius * 0.1;

    // this line will get actual partial completeness - set this variable to something else if you want to test.
    var partialCompleteness = [];
    var partialCompleteElements=document.getElementsByClassName("partial-completeness");
    for(var i=0;i<partialCompleteElements.length;i++){
        var partialComplete=Number(partialCompleteElements[i].innerHTML)===NaN?0:
            Number(partialCompleteElements[i].innerHTML);

        partialCompleteness.push(partialComplete);
    }

    var dimension = (2 * radius) + (2 * padding);
    var translateVar = (radius + padding) * 0.5;

    var internalGraphicContainers=document.getElementsByClassName("internal-graphics-container");
    for(var i=0;i<internalGraphicContainers.length;i++){
        var svg = d3.select(internalGraphicContainers[i])
            .attr("width", dimension)
            .attr("height", dimension)
            .append("g");

        var stroke = radius * 0.2;
        var circleGrouping = svg.append("g").attr("class", "project-badge-circle-grouping").attr("stroke-width", stroke + "px");
        var partialGrouping = svg.append("g").attr("class", "project-badge-partial-grouping").attr("stroke-width", stroke + "px");

        drawD3PartialCircle(circleGrouping, ["project-badge-circle"], radius, padding, 1);
        drawD3PartialCircle(partialGrouping, ["project-badge-line"], radius, padding, partialCompleteness[i]);

    }

};