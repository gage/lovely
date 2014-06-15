
$(document).ready(function(){
    $('a.scrollTo').each(function(idx,el){
        //bookmark style href "#foo" already had the '#' character.
        var id_target = $(el).attr('href'); 
        var duration = $(el).attr('duration');
        $(el).click(function(){
           $.scrollTo( id_target, duration  );
        });
    });
});
