$(document).ready(function(){

    //social communication
    
    function itemclick(e){
        e.preventDefault();
	$(".ue-hp-top-website a").not($(this)).fadeOut();//animate({width:0});
    }

    //homepage scroll

    var infonum=2;
    var scrollpath={
         0:"../../static/img/hp-topbg1.jpg",
         1:"../../static/img/hp-topbg2.jpg",
         2:"../../static/img/hp-topbg3.jpg"
    }
    $(".ue-hp-top-scoll span").click(function(){
	$(".ue-hp-top-scoll span").removeClass("pointnow");
	$(this).addClass("pointnow");
	$(".ue-hp-top-info li").hide();
	$(".ue-hp-top-info li").eq(infonum-$(this).index()).show();
	$(".ue-hp-top").css({background:"url("+scrollpath[infonum-$(this).index()]+")"});
        if($(this).index() == 0) $(".ue-hp-top-website a").bind("click",itemclick);
    })
    
    //item focus on

    if(location.href.match(/\/([0-9]+)\/records/)) $(".ue-hp-top-nav-record").removeClass("ue-hp-top-nav-record").addClass("ue-hp-top-nav-record-focus");
    else if(location.href.match(/\/([0-9]+)\/works/)) $(".ue-hp-top-nav-work").removeClass("ue-hp-top-nav-work").addClass("ue-hp-top-nav-work-focus");
    else if(location.href.match(/\/([0-9]+)\/profile/)) $(".ue-hp-top-nav-info").removeClass("ue-hp-top-nav-info").addClass("ue-hp-top-nav-info-focus");

   //mouseenter show and mouseleave hide
    function meshow() {
	$(".ue-hp-top-v p").show();
	$(".ue-hp-top-v span").unbind("mouseenter",meshow);
	$(".ue-hp-top-v span").bind("mouseleave",mlhide)
    }
    function mlhide() {
	$(".ue-hp-top-v p").hide();
        $(".ue-hp-top-v span").unbind("mouseleave",mlhide)
	$(".ue-hp-top-v span").bind("mouseenter",meshow);
    }
    $(".ue-hp-top-v span").bind("mouseenter",meshow);

   
})