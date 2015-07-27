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
     * This function defines what happens when the different categories are clicked in the
     * 'my impact' section on the dashboard. The category that is clicked is made inactive or active,
     * and then an AJAX request is made. The view this AJAX reqest is sent to updates the
     * preferred_categories attribute of this user.
     */
    $(".category-option-container").click(function() {
        $(this).toggleClass("active");
        var allActiveCategories = $(".category-option-container.active");
        var categoryData = {};

        for (var i = 0; i < allActiveCategories.length; i += 1) {
            var categoryID = $(allActiveCategories[i]).data("category-id");
            categoryData[categoryID] = '';
        }

        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: window.categoryURL,
            method: "POST",
            data: categoryData,
            headers: {"X-CSRFToken": csrftoken},
            error: function (xhr, textStatus, thrownError){
                $(this).toggleClass("active");
                alert("Please try again.");
            },
        });
    });

    /**
     * Copied from the Django documentation. Checks if a method needs a csrf token.
     * Copied from: https://docs.djangoproject.com/en/1.6/ref/contrib/csrf/
     * @param {String} method - The name of a method.
     */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    /**
     * Copied from the Django documentation. Returns an appropriate cookie.
     * Copied from: https://docs.djangoproject.com/en/1.6/ref/contrib/csrf/
     * @param {String} name - type of cookie. In this case, we will always use 'csrftoken'.
     */
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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
    var TABLET_PORTRAIT_BREAKPOINT = 800; // pixels width
    $(".dashboard-data-link").click(function() {
        $(".dashboard-data-link.active").removeClass("active");
        $(this).addClass("active");
        // deletes repayment and funding progress for the current project
        dashboardRepayment.deleteCurrentCircles();
        dashboardFunding.deleteCurrentCircles();
        $(".dashboard-data-section-current").removeClass("dashboard-data-section-current");
        var sectionToShow = $(".dashboard-data-section-" + $(this).data("section"));
        sectionToShow.addClass("dashboard-data-section-current");

        // draws repayment and funding progress for the project we are switching to
        dashboardRepayment.draw();
        dashboardFunding.draw();

        // if we're in an orientation where we should collapse the sidebar, collapse it.
        if ($(window).width() < TABLET_PORTRAIT_BREAKPOINT) {
            $(".dashboard-sidebar").attr("style", "width: 0");
        }
    });

    /**
     * This function defines what happens when a sidebar close toggle is clicked. A sidebar close
     * toggle, in this context, means anything that will cause the sidebar to be closed: this
     * includes the x button at the top right of the sidebar and any link to projects on the sidebar,
     * since when you click a project, it should automatically close the sidebar so you can actually
     * see the project.
     *
     * To implement closing, we add a style attribute to the element which sets the width to zero.
     * When we repoen the sidebar, we'll remove that style element, setting the width back to whatever
     * it was before.
     *
     * Note that if we ever need a significant style="..." attribute on the element, this function will
     * mess that up.
     */
    $(".sidebar-toggle-close").click(function() {
        $(".dashboard-sidebar").attr("style", "width: 0");
        $(".dashboard-sidebar-back-overlay").attr("style", "display: none");
    });

    /**
     * This function defines what happens when a sidebar open toggle is clicked. Currently, the only way
     * to open the sidebar is by clicking the hamburger icon in the dashboard project container - this icon
     * is the only sidebar open toggle.
     *
     * As described above, we remove the style attribute to open up the sidebar again when the toggle is
     * clicked.
     */
    $(".sidebar-toggle-open").click(function() {
        $(".dashboard-sidebar").removeAttr("style");
        $(".dashboard-sidebar-back-overlay").removeAttr("style");
    });

    /**
     * When we resize the window, it might be resized to a width in which we don't want the dashboard sidebar
     * to float anymore, and instead want it to stay fixed on the left side of the screen. In order to enforce
     * this we hook into the window resize event and reset the sidebar's style if the new window size is
     * big enough.
     */
    $(window).resize(function () {
        if ($(window).width() >= TABLET_PORTRAIT_BREAKPOINT) {
            $(".dashboard-sidebar").removeAttr("style");
        }
    });
});
