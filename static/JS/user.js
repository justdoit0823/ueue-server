// user setting

var indexlist={
    "avatar" : 1,
    "basic" : 0,
    "contact" : 2,
    "password" : 3,
    "domain" : 4,
    "auth" : 5,
    "confirm" : 6,
    "realname" : 6
}

$(document).ready(function(){

    var indexkey=location.href.substring(location.href.lastIndexOf('/')+1).split('-')[1];
    if(indexkey == undefined) alert("select item error!");
    else select_item_on($(".user-nav a"),indexlist[indexkey],"active");

        $(".user-normal-div span").click(function(){
                $(this).hide();
                $(this).prev().focus();
        });

        $(".user-normal-div input").blur(function(){
                if(!$(this).val()) $(this).next().show();
        });

        $(".user-normal-div input").focus(function(){
                $(this).next().hide();
        });
	
        $(".user-normal-div input").each(function(index){
                if($(this).val()) $(this).next().hide();
                else $(this).next().show();
        });
        
        $(".user-secrecy").click(function(){
		$(".user-focuson span").fadeOut(200);
	  	$(".user-focuson").removeClass("user-focuson");
		$(this).children('span').css("display","block")
		$(this).addClass("user-focuson");
	});

	$(".authorize-options a").click(function(){
             $(this).parent().prev().text($(this).text());
             $(this).parent().prev().attr("option",$(this).attr("option"));
        })
})