// content review

$(document).ready(function(){


    //post user discuss

    $(".yz-idx-module-discus-sub").click(function(){
	
	var settings={

	    url:location.href,

	    type:"post",

	    dataType:"json",

	    data:{'_xsrf':$("input[name='_xsrf']").val(),'rcontent':$(".yz-idx-module-discus-ta textarea").val()},

	    error:function(jq,data,error){
		alert(data);
	    },
	    success:function(result){
		if(result.status){
		    alert("评论成功！");
		    $(".yz-idx-module-discus-sub").val("发言");
		    $(".yz-idx-module-discus-sub").attr('disabled','');
		    $(result.msg).appendTo(".yz-idx-module-discus-ul");
		}
		else{
		    alert(result.msg);
		}
	    }
	}
	$.ajax(settings);
    })
   /*$(".yz-idx-module-discusbox form").ajaxForm({
                            dataType:"json",
                            beforeSubmit:function(a,f,o){
			       var rcontent=$("#review-content-tx").val();
                               if(!rcontent){
                                     alert("请写下你的评论");
                                     return false;
                               }
                               $(".yz-idx-module-discus-sub").val("发言中...");
                               $(".yz-idx-module-discus-sub").attr('disabled','disabled');
                            },
                            error:function(jq,data,errorThrow){
                                    alert(data);
                            },
                            success:function(result){
                               if(result.status){
                                 alert("评论成功！");
                                 $(".yz-idx-module-discus-sub").val("发言");
                                 $(".yz-idx-module-discus-sub").attr('disabled','');
                                 //$("#review-content-tx").val("欢迎各抒己见");
                                 $(result.msg).appendTo(".yz-idx-module-discus-ul");
                               }
                               else{
                                 alert(result.msg);
                               }
                            }
                })*/
    //share to sinaweibo

     $(".yz-csina").click(function(){
      var param={
            url:location.href,
            type:'3',
            count:'1',
            appkey:'',
            title:$(".showct-ct-title-p").text(),
            pic:'',
            language:'zh_cn',
            rnd:new Date().valueOf()
      }
      var temp=[];
      for(var p in param) temp.push(p+'='+encodeURIComponent(param[p] || ''));
      var url="http://service.weibo.com/share/share.php?"+temp.join("&");
      window.open(url,"分享到微博-新浪微博-随时随地分享身边的新鲜事","width=650,height=500");
    })
    $(".yz-ctencent").click(function(){
      var param={
            url:location.href,
            type:'3',
            count:'1',
            appkey:'',
            title:$(".showct-ct-title-p").text(),
            pic:'',
            language:'zh_cn',
            rnd:new Date().valueOf()
      }
      var temp=[];
      for(var p in param) temp.push(p+'='+encodeURIComponent(param[p] || ''));
      var url="http://service.weibo.com/share/share.php?"+temp.join("&");
      window.open(url,"分享到微博-腾讯微博-随时随地分享身边的新鲜事","width=650,height=500");
    })
})