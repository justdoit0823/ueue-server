

// works and events ajax requesturl

var workrqturl="/works";

var eventrqturl="/records";

var requesttype=-1;


//init texts content

function inittexts(list){

    texts = list;

}

//load the search label

function loadlable(){

    var tags,search;
    if(location.search.length > 0) search = location.search.substring(1);
    if(search != undefined && search.length > 0) tags = search.split('&');
    for(i in tags){
	item = tags[i].split('=');
	if(item && item[0] && item[1]){
	    if($(".yz-idx-line").css('display') == 'none'){
		$(".yz-idx-line").show();
		$(".yz-idx-line .wp1000").append("<div class='z cl yz-idx-line-p'></div>");
	    }
	    var cls,text,data;
	    cls = 'yz-work-lable-' + item[0];
	    if(item[0] == 'trade'){
		text = decodeURIComponent(item[1]);
		data = item[0] + '=' + text;
	    }
	    else{
		text = texts[item[0]][item[1]];
		data = item[0] + '=' + item[1];
	    }
	    addlable(cls,text,data);
	}
    }
}

function addlable(cls,text,data){

    var lable = "<p>\
		         <span class='"+cls+"'>"+text+"</span>\
                         <a data='"+data+"'></a>\
		 </p>";
    $('.yz-idx-line-p').append(lable);
    $(".yz-idx-line-p p").last().find("a").bind("click",dellable);
}    

function dellable(){

    if(location.search.length > 0){

	var s = location.search.substring(1).split('&');

	var i = $(this).parent().index();

	console.log(i);

	if(i == undefined) i = 0;

	//else i;

	console.log(i);

	s.splice(i,1);

	if(s.length > 1) location.search = '?' + s.join('&');

	else if(s.length = 1) location.search = '?' + s[0];

	else location.search = "";
	
    }
          
}



$(document).ready(function(){
	$(document).click(function(e){
	  if($(e.target).is(".list-focuson")){
	   return false;
	  }
	  $(".js-list-1").fadeOut(200);
	  $(".js-list span").removeClass("list-focuson");
	 });
	 
	$(".js-list span").click(function(){
		if(!$(this).hasClass("list-focuson")){
		$(".js-list-1").fadeOut(200);
		$(this).parent('.js-list').find(".js-list-1").fadeIn(200).animate({paddingTop:"10px"},50).animate({paddingTop:"0px"},50).animate({paddingTop:"5px"},50).animate({paddingTop:"0px"},50);
		$(".js-list span").removeClass("list-focuson");
		$(this).addClass("list-focuson");}
	});
	
	
	
	
		$('.yz-idx-event-search-tag2-list-title a').mouseover(function(){ 
 
		$(this).addClass("yz-idx-event-search-tag2-list-title-on").siblings().removeClass(); 
 
		$("."+$(this).attr("id")).show().siblings().hide();
	});
	
	$('.yz-idx-show-search-tag2-list-title a').mouseover(function(){ 
 
		$(this).addClass("yz-idx-show-search-tag2-list-title-on").siblings().removeClass(); 
 
		$("."+$(this).attr("id")).show().siblings().hide();
	});

        var pagelen=5;
        var max=50;
        $(".yz-page-num").click(function(){
            var thisnum=parseInt($(this).text());
            var curnum=parseInt($(".yz-page-focus").text());
            var curidx=$(".yz-page-num").index($(this))+1;
            if((max-pagelen+curidx-1 >= thisnum && thisnum > curnum) || (thisnum > curidx && thisnum < curnum)){
                for(var i=0;i < pagelen;i++){
                    var num=thisnum-(pagelen-1)/2+i;
                    if(num < 10) num="0"+num
                    $(".yz-page-num").eq(i).text(num);
                }
            }
            else{
                $(".yz-page-focus").removeClass("yz-page-focus");
                $(this).addClass("yz-page-focus");
            }
        })
        $(".yz-page-next").click(function(){
            var curidx=parseInt($(".yz-page-focus").text())+pagelen;
            for(var i=0;i < pagelen;i++){
                $(".yz-page-num").eq(i).text(curidx-(pagelen-1)/2+i);
            }
        })
        $(".yz-page-prev").click(function(){
            var curidx=parseInt($(".yz-page-focus").text())-pagelen;
            for(var i=0;i < pagelen;i++){
                $(".yz-page-num").eq(i).text(curidx-(pagelen-1)/2+i);
            }
        })
});

$(document).ready(function() {
	
    var sideArray = new Array(1,2);
	showSideBar(sideArray);

	var slideLength = $(".ue-index-slide-item").length;	   	//  total 3-cols slides
	var slideIndex  = 0;					//  default index -- initial showed slide	
	var	slideTimer, timerInterval = 4000;
	var clickIndex;
	var fadeTime = 500;

	$(".ue-index-slide").hover(function() {
		clearInterval(slideTimer);
	}, function(){
		slideTimer = setInterval(function() {
			if (slideIndex == slideLength - 1) {
				showSlide(0);
				slideIndex = -1;
			} else {
				showSlide(slideIndex + 1);
			};

			slideIndex++;
		}, timerInterval);
	}).trigger("mouseleave");

	$(".ue-slide-left").click(function() {

		clickIndex = slideIndex == 0 ? slideLength - 1 : slideIndex - 1;		
		showSlide(clickIndex);
		slideIndex = clickIndex;
	});

	$(".ue-slide-right").click(function() {

		clickIndex = slideIndex == slideLength - 1 ?  0 : slideIndex + 1;		
		showSlide(clickIndex);
		slideIndex = clickIndex;
	});

	//  show the spicified slide and update the nav-slstyle
	function showSlide(index)
	{
		$(".ue-index-slide-item").eq(slideIndex).fadeOut(fadeTime);
		$(".ue-index-slide-item").eq(index).fadeIn(fadeTime);
	}

});

//editor load

function loadeditor(){
    $(".yz-meb-btn1").unbind("click");
    $(".editor-back").unbind("click");
    if($(".ue-hdbg-editor").css("height") == "142px"){
	$(".ue-hdbg-editor").css({"border-bottom":"none"});
	$(".ue-hdbg-editor").animate({"height":"0"},200,function(){$(".yz-meb-btn1").bind("click",loadeditor);});
    }
    else{
	$(".ue-hdbg-editor").css({"border-bottom":"1px solid #CCC"});
	$(".ue-hdbg-editor").animate({"height":"142"},200,function(){$(".yz-meb-btn1").bind("click",loadeditor);$(".editor-back").bind("click",loadeditor);});
    }
}

$(document).ready(function(){
    $(".ue-hdbg-editor").css({"height":"0"});
    $(".ue-hdbg-editor").css({"border-bottom":"none"});
    $(".yz-meb-btn1").bind("click",loadeditor);
    $(".ue-people-post").click(function(){
        $(".yz-meb-btn1").trigger("click");
    })
})
