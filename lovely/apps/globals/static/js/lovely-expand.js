
$(document).ready(function(){

    jQuery(".wrapper_test_expand .content").hide();

    function bindCollapse(idx,el){
        $(el).toggle(
            function(event)
            {
                $(".wrapper_test_expand .readmore").eq(idx).hide();
                $(".wrapper_test_expand .readless").eq(idx).show();
                $(el).stop(true,true);
                $(".wrapper_test_expand .content").eq(idx).slideDown('500',function(){
                });
            },
            function(event)
            {

                $(el).stop(true,true);
                $(".wrapper_test_expand .content").eq(idx).slideUp('500',function(){
                    $(".wrapper_test_expand .readmore").eq(idx).show();
                    $(".wrapper_test_expand .readless").eq(idx).hide();
                });
            }
        );
    }

    $(".wrapper_test_expand .collapse").each(function(idx,el){
        bindCollapse(idx,el);
    });

    function bindContent(idx,el)
    {
        $(el).click(function(event){
            if($(this).is(':visible'))
            {
                var THIS = this;

                // erase previous toggle.
                $(".wrapper_test_expand .collapse").eq(idx).unbind();
                bindCollapse(idx,$('.collapse').eq(idx));                

                $(this).slideUp('500',function(){
                    $(THIS).stop();
                    $(".wrapper_test_expand .readmore").eq(idx).show();
                    $(".wrapper_test_expand .readless").eq(idx).hide();
                });
            }
        });
    }

    $('.wrapper_test_expand .content').each(function(idx,el){
        bindContent(idx,el);
    });

});
