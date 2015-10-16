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


    var windowWidth=$(document).width();

    var radius=120;
    var radiusRatio=1;

    // These conditions are for multiple windows sizes. Radius is scaled down in stepped mode as
    // windows size decreases.
    if(windowWidth > 960){
        radiusRatio=1.8;
    }
    else if(windowWidth<=960 && windowWidth>640){
        radiusRatio=2.1;
    }
    else if(windowWidth<=640){
        radiusRatio=2.5;
    }

    radius=radius/radiusRatio;
    setTextSize(radius);

    resizeIframe();
    drawCircle(radius,radiusRatio);


};
