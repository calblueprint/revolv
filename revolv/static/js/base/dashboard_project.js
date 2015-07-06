/**
 * This file renders the svg circles for the repayment modules for the project view
 * on the user dashboards. It defines and then creates a DashboardCircles object
 * that handles the logic for drawing repayment progress. The DashboardCircles object is
 * used in dashboard.js, where the logic for switching tabs and projects is taken care of.
 */
function DashboardRepaymentCircles() {
    /**
     * Deletes circles for the currently active project. Called when switching projects on the dashboard.
     */
    this.deleteCurrentCircles = function() {
        $(".dashboard-data-section-current .repayment-progress-container .repayment-badge-circle-grouping").remove();
        $(".dashboard-data-section-current .repayment-progress-container .repayment-badge-partial-grouping").remove();
        $(".dashboard-data-section-current .repayment-progress-container .repayment-badge-circle").remove();
        $(".dashboard-data-section-current .repayment-progress-container .repayment-badge-line" ).remove();
        $(".dashboard-data-section-current .outside-circle" ).remove();
    };

    /**
     * Resizes the text inside the speedometer.
     */
    this.setTextSize = function(radius) {
        var percentage_size = 3 * radius / 100;
        var repaid_size = percentage_size * 0.5;

        d3.selectAll(".percentage-text").attr("style", "font-size:" + percentage_size + "rem");
        d3.selectAll(".repaid").attr("font-size", "font-size:" + repaid_size + "rem");
    };

    /**
     * Dynamically resizes text inside the speedometer, draws an outside circle, and draws an inner
     * partial circle based on the width of the existing screen.
     */
    this.draw = function() {
        var radius = $(document).width() * 0.12;
        this.setTextSize(radius);

        var outsideCircle = d3.select(".dashboard-data-section-current .repayment-progress-container .svg-graphics-container");
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

            if (radius > 80 ) {
                radius = 80;
                outsideCircleRadius = 1.1 * radius;
                outsideCircle.attr("r", outsideCircleRadius);
            }

            if (radius < 60 ) {
                radius = 60;
                outsideCircleRadius = 1.1 * radius;
                outsideCircle.attr("r", outsideCircleRadius);
            }
        }
        this.setTextSize(radius);
        var padding = radius * 0.1;

        // this line will get actual partial completeness - set this variable to something else if you want to test.
        var partialCompleteness = d3.select(".dashboard-data-section-current .repayment-progress-container .percentage-container");
        if (!partialCompleteness.empty()) {
            partialCompleteness = parseFloat(partialCompleteness.text());
        } else {
            partialCompleteness = 0.0;
        }

        var dimension = (2 * radius) + (2 * padding);
        var translateVar = (radius + padding) * 0.5;

        var svg = d3.select(".dashboard-data-section-current .repayment-progress-container .internal-graphics-container");
        // we have this check whether it is null because the currently selected project might not be completed
        if (!svg.empty()) {
            svg = svg.attr("width", dimension)
                .attr("height", dimension)
                .append("g");

            var stroke = radius * 0.2;
            var circleGrouping = svg.append("g").attr("class", "repayment-badge-circle-grouping").attr("stroke-width", stroke + "px");
            var partialGrouping = svg.append("g").attr("class", "repayment-badge-partial-grouping").attr("stroke-width", stroke + "px");

            drawD3PartialCircle(circleGrouping, ["repayment-badge-circle"], radius, padding, 1);
            drawD3PartialCircle(partialGrouping, ["repayment-badge-line"], radius, padding, partialCompleteness);
        }
    };
}

function DashboardFundingCircles() {
    /**
     * Deletes circles for the currently active project. Called when switching projects on the dashboard.
     */
    this.deleteCurrentCircles = function() {
        $(".dashboard-data-section-current .funding-progress-container .funding-badge-circle-grouping").remove();
        $(".dashboard-data-section-current .funding-progress-container .funding-badge-partial-grouping").remove();
        $(".dashboard-data-section-current .funding-progress-container .funding-badge-circle").remove();
        $(".dashboard-data-section-current .funding-progress-container .funding-badge-line" ).remove();
        $(".dashboard-data-section-current .outside-circle" ).remove();
    };

    /**
     * Resizes the text inside the speedometer.
     */
    this.setTextSize = function(radius) {
        var percentage_size = 3 * radius / 100;
        var repaid_size = percentage_size * 0.5;

        d3.selectAll(".percentage-text").attr("style", "font-size:" + percentage_size + "rem");
        d3.selectAll(".repaid").attr("font-size", "font-size:" + repaid_size + "rem");
    };

    /**
     * Dynamically resizes text inside the speedometer, draws an outside circle, and draws an inner
     * partial circle based on the width of the existing screen.
     */
    this.draw = function() {
        var radius = $(document).width() * 0.12;
        this.setTextSize(radius);

        var outsideCircle = d3.select(".dashboard-data-section-current .funding-progress-container .svg-graphics-container");
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

            if (radius > 60 ) {
                radius = 60;
                outsideCircleRadius = 1.1 * radius;
                outsideCircle.attr("r", outsideCircleRadius);
            }

            if (radius < 45 ) {
                radius = 45;
                outsideCircleRadius = 1.1 * radius;
                outsideCircle.attr("r", outsideCircleRadius);
            }
        }
        this.setTextSize(radius);
        var padding = radius * 0.1;

        // this line will get actual partial completeness - set this variable to something else if you want to test.
        var partialCompleteness = d3.select(".dashboard-data-section-current .funding-progress-container .percentage-container");
        if (!partialCompleteness.empty()) {
            partialCompleteness = parseFloat(partialCompleteness.text());
        } else {
            partialCompleteness = 0.0;
        }

        var dimension = (2 * radius) + (2 * padding);
        var translateVar = (radius + padding) * 0.5;

        var svg = d3.select(".dashboard-data-section-current .funding-progress-container .internal-graphics-container");
        // we have this check whether it is null because the currently selected project might not be completed
        if (!svg.empty()) {
            svg = svg.attr("width", dimension)
                .attr("height", dimension)
                .append("g");

            var stroke = radius * 0.2;
            var circleGrouping = svg.append("g").attr("class", "funding-badge-circle-grouping").attr("stroke-width", stroke + "px");
            var partialGrouping = svg.append("g").attr("class", "funding-badge-partial-grouping").attr("stroke-width", stroke + "px");

            drawD3PartialCircle(circleGrouping, ["funding-badge-circle"], radius, padding, 1);
            drawD3PartialCircle(partialGrouping, ["funding-badge-line"], radius, padding, partialCompleteness);
        }
    };
}

// initializes a dashboard repayment circles object
var dashboardRepayment = new DashboardRepaymentCircles();

// initializes a dashboard funding circles object
var dashboardFunding = new DashboardFundingCircles();

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
