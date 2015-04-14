$(document).ready(function () {
    $(".dashboard-sidebar-chevron").click(function() {
        var $this = $(this);
        if ($this.data("state") === "expanded") {
            $(".role-select-options").slideUp();
            $this.data("state", "collapsed");
            $this.removeClass("fa-rotate-180");
        } else {
            $(".role-select-options").slideDown();
            $this.data("state", "expanded");
            $this.addClass("fa-rotate-180");
        }
    });

    $(".dashboard-data-link").click(function() {
        $(".dashboard-data-link.active").removeClass("active");
        $(this).addClass("active");
        $(".dashboard-data-section-current").removeClass("dashboard-data-section-current");
        var sectionToShow = $(".dashboard-data-section-" + $(this).data("section"));
        sectionToShow.addClass("dashboard-data-section-current");
    });
});
