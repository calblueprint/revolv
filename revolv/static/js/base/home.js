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
 * Dynamically resizes text inside the speedometer, resizes the iframe, draws an outside circle, and draws an inner
 * partial circle based on the width of the existing screen.
 */
var draw = function() {

    var outsideCircles = d3.selectAll(".svg-graphics-container");
    var windowWidth=$(document).width();

    //If number of circles are greater than one, it means that multiple projects are active.
    //Hence set the radius circle
    var activeProjectCount=-1;
    if(outsideCircles.length>0){
        activeProjectCount=outsideCircles[0].length;
    }

    // In Home Page, there can be multiple active projects, hence more than 1 project in a row.
    // radiusRatio is used to take care of multiple active projects as well as

    // This value donates the radius of circle where there are multiple active projects and also
    // windowWidth is more than 960px
    // This value is just logical, it is further changed in drawCirlce function of util.js
    var radius=200;

    // If there is only one active project, radius is varied as the screen changes.
    if(activeProjectCount==1) {
         radius = windowWidth * 0.12;
    }
    var radiusRatio=1;


    // In case there are multiple projects
    if(activeProjectCount>1){
        // These conditions takes care of various window sizes for multiple projects cases.
        if(windowWidth > 960){
        radiusRatio=1.8;
        }
        else if(windowWidth<=960 && windowWidth>640){
            radiusRatio=2.1;
        }
        else if(windowWidth<=640){
            radiusRatio=2.5;
        }
    }

    radius=radius/radiusRatio;
    setTextSize(radius);

    resizeIframe();
    // call drawCircle function of util.js
    drawCircle(radius,radiusRatio);
};