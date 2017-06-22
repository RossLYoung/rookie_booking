


$(document).ready(function() {


    //////////////////////////////////////////////////////////
    var all_comment_toggles = $('[id^=show-comment-]');

    all_comment_toggles.click(function(event) {

        //gets called by click event as both span and parent anchor fire
        //nasty way to ignore one of the events
        if(this.localName == 'a'){

            var id = event.target.id.replace( /^\D+/g, '');
            //console.log(id);
            toggleCommentButton(id);
        }
    });

    //////////////////////////////////////////////////////////
    function toggleCommentButton(id){

        //bootstrap collapse/show is wired up using data-attributes, so only button styling

        var toggle_text = $("#show-comment-text-"+id)[0];
        var toggle_icon = $("#show-comment-icon-"+id)[0];
        var form = $("#form-"+id);

        $(toggle_icon).toggleClass("fa-angle-double-down").toggleClass("fa-angle-double-up");

        if (toggle_text.innerText == 'reply'){
            toggle_text.innerText = 'hide';

            //not working
            var next_textarea = $(form).find('textarea');
            if(next_textarea){
                setTimeout(function() {
                  $(next_textarea).focus();
                }, 0);
            }
        }
        else{
            toggle_text.innerText = 'reply';
        }
    }

    function toggleCommentButtonReset(id){
        var toggle_text = $("#show-comment-text-"+id)[0];
        var toggle_icon = $("#show-comment-icon-"+id)[0];

        toggle_text.innerText = 'reply';
        $(toggle_icon).addClass("fa-angle-double-down");
        $(toggle_icon).removeClass("fa-angle-double-up");
    }

    //////////////////////////////////////////////////////////
    var all_expand_collapse_toggles = $('[id^=expand-collapse-]');

    all_expand_collapse_toggles.click(function(event) {

        var id = this.id.replace( /^\D+/g, '');

        var icon_span = $("#expand-collapse-"+id + " span");
        var comment_bottom = $("#comment-bottom-"+id);
        var form = $("#form-"+id);

        var comment_container = form.closest('div[class^="comment-container-"]');

        if ($(icon_span).hasClass("fa-minus")) {

            comment_bottom.toggle();
            toggleNestedComments(comment_container, 'hide');

            if(form.is(':visible')){
                //alert('hiding!');
                form.collapse('hide');
            }

            toggleCommentButtonReset(id);

        }
        else{
            comment_bottom.toggle();
            toggleNestedComments(comment_container, 'show')        }

        //needs to be last as class is checked above
        icon_span.toggleClass("fa-plus").toggleClass('fa-minus');

        return false
    });

    function toggleNestedComments(parent_container, direction){

        var all_child_containers = $(parent_container).find('[class^="comment-container-"]');

        if (direction == 'hide') {
           //$(all_child_containers).hide();
           $(all_child_containers).css('display', 'none');
        }
        else{
           //$(all_child_containers).show();
           $(all_child_containers).css('display', 'block');
        }
    }


}());
