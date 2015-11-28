/**
 * This class renders the svg circles for the project view on the user dashboards.
 * It defines and initializes a DashboardCircles object that handles the logic for
 * drawing progress (funding or repayment). The DashboardCircles object is
 * used in dashboard.js, where the logic for switching tabs and projects is taken care of.
 *
 * Parameters:
 * @param int minRadius - the minimum radius of the svg circle
 * @param int maxRadius - the maximum radius of the svg circle
 * @param Object htmlClassNames - an object mapping specific component names of an svg circle
 * to the html class name of that component. Used for assigning class names for HTML
 * HTML components and to generate CSS selectors for HTML components.
 * (Look at how they're used in the class and to construct objects for better reference)
 */
function DashboardCircles(minRadius, maxRadius, htmlClassNames) {
    /**
     * Deletes circles for the currently active project. Called when switching projects on the dashboard.
     */
    this.deleteCurrentCircles = function() {
        $(this.generateSelector(htmlClassNames["badgeCircle"])).remove();
        $(this.generateSelector(htmlClassNames["badgeLine"])).remove();
        $(this.generateSelector(htmlClassNames["outsideCircle"])).remove();
        $(this.generateSelector(htmlClassNames["badgeGroupingContainer"])).remove();
    };

    /**
     * Generates a CSS selector for the className of interest. Most CSS selectors for
     * the DashboardCircles object are prepended with the current section and the
     * container for that specific circle.
     *
     */
    this.generateSelector = function(className) {
        return "." + htmlClassNames["currentSection"] + " ." + htmlClassNames["container"] + " ." + className;
    };

    /**
     * Resizes the text inside the speedometer.
     */
    this.setTextSize = function(radius) {
        var percentageSize = 3 * radius / 100;
        var circleTextSize = percentageSize * 0.5;

        d3.selectAll(this.generateSelector(htmlClassNames["percentageText"]))
            .attr("style", "font-size:" + percentageSize + "rem");
        d3.selectAll(this.generateSelector(htmlClassNames["circleText"]))
            .attr("font-size", "font-size:" + circleTextSize + "rem");
    };

    /**
     * Dynamically resizes text inside the speedometer, draws an outside circle, and draws an inner
     * partial circle based on the width of the existing screen.
     */
    this.draw = function() {
        var radius = $(document).width() * 0.12;
        this.setTextSize(radius);

        var outsideCircle = d3.select(this.generateSelector(htmlClassNames["svgContainer"]));
        // we have this check whether it is null because the currently selected project might not be completed
        if (!outsideCircle.empty()) {
            var outsideCircleRadius = 1.1 * radius;
            outsideCircle = outsideCircle.append("circle")
                .attr("class", "outside-circle")
                .attr("cx", "50%")
                .attr("cy", "50%")
                .attr("stroke", "#ddd")
                .attr("stroke-width", "3")
                .attr("fill", "white")
                .attr("r", outsideCircleRadius);

            if (radius > maxRadius ) {
                radius = maxRadius;
                outsideCircleRadius = 1.1 * radius;
                outsideCircle.attr("r", outsideCircleRadius);
            }

            if (radius < minRadius ) {
                radius = minRadius;
                outsideCircleRadius = 1.1 * radius;
                outsideCircle.attr("r", outsideCircleRadius);
            }
        }
        this.setTextSize(radius);
        var padding = radius * 0.1;

        // this line will get actual partial completeness - set this variable to something else if you want to test.
        var partialCompleteness = d3.select(this.generateSelector(htmlClassNames["percentageContainer"]));
        if (!partialCompleteness.empty()) {
            partialCompleteness = parseFloat(partialCompleteness.text());
        } else {
            partialCompleteness = 0.0;
        }

        var dimension = (2 * radius) + (2 * padding);
        var translateVar = (radius + padding) * 0.5;

        var svg = d3.select(this.generateSelector(htmlClassNames["internalGraphicsContainer"]));
        // we have this check whether it is null because the currently selected project might not be completed
        if (!svg.empty()) {
            svg = svg.attr("width", dimension)
                .attr("height", dimension)
                .append("g").attr("class", htmlClassNames["badgeGroupingContainer"]);

            var stroke = radius * 0.2;
            var circleGrouping = svg.append("g").attr("class", htmlClassNames["badgeCircleGrouping"]).attr("stroke-width", stroke + "px");
            var partialGrouping = svg.append("g").attr("class", htmlClassNames["badgePartialGrouping"]).attr("stroke-width", stroke + "px");

            drawD3PartialCircle(circleGrouping, [htmlClassNames["badgeCircle"]], radius, padding, 1);
            drawD3PartialCircle(partialGrouping, [htmlClassNames["badgeLine"]], radius, padding, partialCompleteness);
        }
    };
}

// initializes a dashboard circles object for rendering Repayment circles.
var repaymentClassNames = {
    "badgeCircle": "repayment-badge-circle",
    "badgeLine": "repayment-badge-line",
    "badgeCircleGrouping": "repayment-badge-circle-grouping",
    "badgePartialGrouping": "repayment-badge-partial-grouping",
    "badgeGroupingContainer": "badge-grouping-container",
    "currentSection": "dashboard-data-section-current ",
    "container": "repayment-progress-container ",
    "svgContainer": "dashboard-svg-graphics-container",
    "percentageContainer": "percentage-container",
    "internalGraphicsContainer": "dashboard-internal-graphics-container",
    "outsideCircle": "outside-circle",
    "circleText": "repaid",
    "percentageText": "percentage-text",
};
var dashboardRepayment = new DashboardCircles(60, 80, repaymentClassNames);

// initializes a dashboard circles object for rendering Funding circles.
var fundingClassNames = {
    "badgeCircle": "funding-badge-circle",
    "badgeLine": "funding-badge-line",
    "badgeCircleGrouping": "funding-badge-circle-grouping",
    "badgePartialGrouping": "funding-badge-partial-grouping",
    "badgeGroupingContainer": "badge-grouping-container",
    "currentSection": "dashboard-data-section-current ",
    "container": "funding-progress-container ",
    "svgContainer": "dashboard-svg-graphics-container",
    "percentageContainer": "percentage-container",
    "internalGraphicsContainer": "dashboard-internal-graphics-container",
    "outsideCircle": "outside-circle",
    "circleText": "funded",
    "percentageText": "percentage-text",
};
var dashboardFunding = new DashboardCircles(60, 60, fundingClassNames);

// binds events and listeners to properly render svg circles
$(document).ready(function () {
    dashboardRepayment.draw();
    dashboardFunding.draw();
});

$( window ).resize(function() {
    dashboardRepayment.deleteCurrentCircles();
    dashboardRepayment.draw();
    dashboardFunding.deleteCurrentCircles();
    dashboardFunding.draw();
});
