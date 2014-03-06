//editor part

var lable="";

var swfu;

$(document).ready(function(){

    $(".editor-post-opentype i").bind("click",switcho2p);

    //add signup

    $(".editor-tags-text").keydown(function(event){
          var val=$(this).val();
	  var idx;
          if(event.keyCode==13 || event.keyCode==32){
	     event.preventDefault();
             if(val){
                var lbs=lable.split(',');
                var is_repeat=false;
                for(i in lbs)
                   if((lbs[i])==val){
                       is_repeat=true;
                       break;
                   }
                if(is_repeat) alert('标签重复');
                else{
                    var add="<span>"+val+"<a onclick='$(this).parent().remove();'></a></span>";
                    $(".editor-tags-name").append(add);
                    $(this).val('');
                    if(!lable) lable=val;
                    else lable+=','+val;
                }
             }
         }
        if(event.keyCode==8){
            if(!val){
		event.preventDefault();
		$(".editor-tags-name span").last().remove();
		idx=lable.lastIndexOf(',');
		if(idx != -1){
		    lable=lable.substring(0,idx);
		}
		else lable="";
            }
         }
     })


    //sign-markup

    $(".editor-cc a").click(function(){
	select_item_on($(".editor-cc a"),$(this).index(),"editor-cc-on");
    })


    //add teammates

    $(".editor-team-addbtn").click(function(){
        var teamlihtml="<li>\
							<input type='text' class='editor-team-id z cl' onKeyDown='if (event.keyCode==13) {}' onBlur='if(this.value==\"\")value=\"账号名\";' onFocus='if(this.value==\"账号名\")value=\"\";' value='账号名'/>\
							<input type='text' class='editor-team-work z cl' onKeyDown='if (event.keyCode==13) {}' onBlur='if(this.value==\"\")value=\"职能描述 如 : 摄影、化妆造型\";' onFocus='if(this.value==\"职能描述 如 : 摄影、化妆造型\")value=\"\";' value='职能描述 如 : 摄影、化妆造型'/>\
							<input type='button' class='editor-team-del y cl'/>\
						</li>";
         $(".editor-team").append(teamlihtml);
         $(".editor-team li").last().children(".editor-team-del").bind("click",function(){
             $(this).parent().remove();
         });
    })

    $(".editor-team-del").click(function(){
         $(this).parent().remove();
    })

})


// function formate the date for the standard

function dateformat(date){
      date=parseInt(date).toString();
      return parseInt(date) < 10 ? "0"+date : date ;
  }

//choose item on

function select_item_on(jqobj,index,classname){
    if($.type(jqobj) != "object"){
	alert("undefined object type!");
	return -1;
    }
    jqobj.removeClass(classname);
    jqobj.eq(index).addClass(classname);
}

//switch to open or private

function switcho2p(){
    if($(this).next().hasClass("editor-sub-btn4")){
	$(this).next().removeClass("editor-sub-btn4").addClass("editor-sub-btn3").text("保密发布");
    }
    else{
	$(this).next().removeClass("editor-sub-btn3").addClass("editor-sub-btn4").text("公开发布");
    }
}


//append uploaded picture

function completeUploadpic(ProgressWrapper,serverData)
{
    ProgressWrapper.removeChild(ProgressWrapper.childNodes[0]);
    serverData=JSON.parse(serverData);
    var editorImage=document.createElement("div");
    editorImage.className="z cl editor-pic-img";
    var editorPicture=document.createElement("img");
    editorPicture.src=serverData.path;
    editorImage.appendChild(editorPicture);
    var editorText=document.createElement("div");
    editorText.className="z cl editor-pic-text";
    var editorArea=document.createElement("textarea");
    editorArea.innerHTML="- 描述 -";
    editorArea.onkeydown=function (event){if (event.keyCode==13) {}};
    editorArea.onblur=function (){if(this.innerHTML == '') this.innerHTML="- 描述 -"};
    editorArea.onfocus=function (){if(this.innerHTML == '- 描述 -') this.innerHTML=""};
    editorText.appendChild(editorArea);
    editorDelete=document.createElement("span");
    editorDelete.className="editor-pic-del";
    editorMove=document.createElement("span");
    editorMove.className="editor-pic-move z cl";
    editorMove.title="按住可以拖动排序哦~";
    editorFront=document.createElement("a");
    editorFront.className="editor-pic-front z cl mgt20";
    editorFront.appendChild(document.createTextNode("选为封面"));
    editorFronton=document.createElement("span");
    editorFronton.className="editor-pic-front-on";
    editorFront.appendChild(editorFronton);
    ProgressWrapper.appendChild(editorImage);
    ProgressWrapper.appendChild(editorText);
    ProgressWrapper.appendChild(editorDelete);
    ProgressWrapper.appendChild(editorMove);
    ProgressWrapper.appendChild(editorFront);
}

// init flash

function initflash(limit){
    if(limit == undefined) return;
    window.onload = function() {
			var settings = {
				flash_url : "/static/flash/swfupload.swf",
				upload_url: "/user/works/multipicupload",
		                post_params: {"_yoez_uid" : get_cookie("_yoez_uid") , "_xsrf_cookie" : get_cookie("_xsrf"),
					      "_xsrf" : $("input[name='_xsrf']").val()},
		                preserve_relative_urls: true,
		                use_query_string: false,
				file_size_limit : limit.size+" MB",
				file_types : "*.png;*.jpg;*.jpeg;*.gif",
				file_types_description : "Image Files",
				file_upload_limit : limit.num,
				file_queue_limit : 0,
				custom_settings : {
					progressTarget : "fsUploadProgress",
					cancelButtonId : "btnCancel"
				},
				debug: false,

				// Button settings
				button_width: "120",
				button_height: "40",
		                button_cursor: "pointer",
				button_placeholder_id: "spanButtonPlaceHolder",
				button_text: '<span class="theFont"></span>',
				button_text_style: ".theFont { font-size: 14; }",
		                button_window_mode: "transparent",
				
				// The event handler functions are defined in handlers.js
				file_queued_handler : fileQueued,
				file_queue_error_handler : fileQueueError,
				file_dialog_complete_handler : fileDialogComplete,
				upload_start_handler : uploadStart,
				upload_progress_handler : uploadProgress,
				upload_error_handler : uploadError,
				upload_success_handler : uploadSuccess,
				upload_complete_handler : uploadComplete,
				queue_complete_handler : queueComplete	// Queue plugin event
			};

			swfu = new SWFUpload(settings);
	     }
}
