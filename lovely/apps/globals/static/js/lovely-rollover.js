
$(document).ready(function(){
    $(".header-section").each(function(idx,el){
        $(el).hover(
             function(){
                $(el).find("img.normal").hide();
                $(el).find("img.rollover").show(); 
             }
            , function(){
                $(el).find("img.normal").show();
                $(el).find("img.rollover").hide(); 
             });
    });
});
