$(document).ready(function () {
    /**
     * This function defines what happens when the chevron in the dashboard sidebar
     * (the "^") is clicked. The area which shows which roles the current user can
     * view the dashboard as (admin, ambassador, or regular donor) is not shown by
     * default, but when the chevron is clicked, the chevron is rotated and the role
     * selection area is shown.
     *
     * When the chevron is clicked again, the role selection area dissapears.
     */
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

    /**
     * This function defines what happens when a dashboard data link is clicked. A data
     * link is defined as any element which, when clicked on, will cause the dashboard to
     * show the page of another project. The element which has a class dashboard-data-link
     * must also define data-section="x" - this will cause the element with .dashboard-data-section-x
     * to be shown and any other element with dashboard-data-section-* to be hidden.
     *
     * This function will also add an "active" class to whichever dashboard data link was
     * clicked on, and remove the "active" class from all other dashboard data links. This
     * works very well for selecting projects via the dashboard sidebar.
     *
     * Note: if we detect that we're in an orientation of a device where we should be collapsing
     * the sidebar when we click a link in it, we also set the sidebar's width to 0 in this
     * function. It's width will be restored to whatever it was previously when the .sidebar-toggle-open
     * is clicked.
     */
    $(".dashboard-data-link").click(function() {
        $(".dashboard-data-link.active").removeClass("active");
        $(this).addClass("active");
        $(".dashboard-data-section-current").removeClass("dashboard-data-section-current");
        var sectionToShow = $(".dashboard-data-section-" + $(this).data("section"));
        sectionToShow.addClass("dashboard-data-section-current");

        // if we're in an orientation where we should collapse the sidebar, collapse it.
        if ($(window).width() < 800) {
            $(".dashboard-sidebar").attr("style", "width: 0");
        }
    });

    $(".sidebar-toggle-close").click(function() {
        $(".dashboard-sidebar").attr("style", "width: 0");
    });

    $(".sidebar-toggle-open").click(function() {
        $(".dashboard-sidebar").removeAttr("style");
    });

    var $firstProject = $(".dashboard-project").first();
    if ($firstProject.length) {
        $firstProject.addClass("dashboard-data-section-current");
        $(".dashboard-sidebar-project-container-" + $firstProject.data("project-id")).addClass("active");
    }
});
