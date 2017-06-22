

$( document ).ready(function() {

    //need to see that this selector is only ever looked up once - only reason to have within .ready()
    var mobile_nav = $("#mobile-nav-dropdown");
    var mobile_nav_collapse = $('#mobile-nav-collapse');
    var nav_expand = "fa-angle-double-down";
    var nav_collapse = "fa-angle-double-up";

    //remove mobile expanded class when going larger (to close mobile nav when portrait to landscape on some devices)
    //bad as it hardcodes a media query breakpoint. Must remember to change in JS if SASS variable changes.
    $(window).resize(function(){
        if($( window ).width() > 768){
            (mobile_nav.removeClass("in"));
            toggle_nav_button_down()
        }
    });

    //Change to work with classToggle
    mobile_nav.on('show.bs.collapse', function () {
        toggle_nav_button_up();
    });
    mobile_nav.on('hide.bs.collapse', function () {
        toggle_nav_button_down()
    });

    //Change to work with classToggle
    function toggle_nav_button_up(){
        //mobile_nav_collapse.toggleClass(nav_expand);
        mobile_nav_collapse.removeClass(nav_expand);
        mobile_nav_collapse.addClass(nav_collapse);
    }
    function toggle_nav_button_down(){
        //mobile_nav_collapse.toggleClass(nav_collapse);
        mobile_nav_collapse.removeClass(nav_collapse);
        mobile_nav_collapse.addClass(nav_expand);
    }

    //hide mobile nav menu if user scrolls up
    //$(this).scroll(function() {
    //    console.log("wooo!");
    //    $(mobile_nav).collapse('hide');
    //    toggle_nav_button_down();
    //});
    /////////////////////////////

    var dropDowns = $('[id^="drop-down"]');

    if(dropDowns.length){
        dropDowns.on('show.bs.collapse', function (event) {
            icon = $(event.target).prev().find("i").last();
            icon.removeClass("fa-angle-down").addClass("fa-angle-up");
        });
        dropDowns.on('hide.bs.collapse', function (event) {
            icon = $(event.target).prev().find("i").last();
            icon.removeClass("fa-angle-up").addClass("fa-angle-down");
        });
    }

    var toast = $('.toast--hidden');
    if (toast.length){toast.slideDown('slow').delay(1500).slideUp('slow');}

});


