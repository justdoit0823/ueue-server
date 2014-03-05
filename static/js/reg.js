//default name length

DEFNAMELEN=16;

$(document).ready(function(){
    function spanclick(){
        $(this).hide();
        $(this).unbind("click");
        $(this).prev().focus();
    }
    $(".rg-box span:not(.rg-agreement-checkbox)").click(function(){
        $(this).hide();
        $(this).unbind("click");
        $(this).prev().focus();
    })
    $(".rg-box input").focus(function(){
        $(this).next().hide();
        $(this).unbind("click");
    })
    $(".rg-box input").blur(function(){
        if(!$(this).val()){
            $(this).next().show();
            $(this).next().bind("click",spanclick);
        }
    })
              var submite,submitu,submitp;
              submite=submitu=submitp=false;
              $("#yoez_reg_f").ajaxForm({
                beforeSubmit: function(a,f,o) {
		            if($(".rg-email input").val().length == 0){
                                    $(".rg-email-t").html("填入一个常用的邮箱");
			            $(".rg-email-t").show("fast");
                                    $(".rg-email input").focus();
			            return false;
		            }
                            if($(".rg-nic input").val().length == 0){
                                    $(".rg-nic-t").html("我们建议使用真实姓名以便知晓和联络");
			            $(".rg-nic-t").show("fast");   
                                    $(".rg-nic input").focus();
			            return false;
		            }
		            if($(".rg-psw input").val().length == 0){
                                    $(".rg-psw-t").html("密码不要少于6位");
			            $(".rg-psw-t").show("fast");
                                    $(".rg-psw input").focus();
			            return false;
		            }
                            else if($(".rg-psw input").val().length < 6){
			            $(".rg-psw-t").html('密码不要少于6位');
			            $(".rg-psw-t").show("fast");
                                    $(".rg-psw input").focus();
			            return false;
		            }
                            if(!submite){
			            $(".rg-email-t").html('请填写有效邮箱');
			            $(".rg-email-t").show("fast");
                                    $(".rg-email input").focus();
                                    return false;
                            }
                            else if(!submitu){
			             $(".rg-nic-t").html('请填写有效用户名');
			             $(".rg-nic-t").show("fast");
                                     $(".rg-nic input").focus();
                                     return false;
                            }
                            else if(!submitp){
			              $(".rg-psw-t").html('请填写有效密码');
			              $(".rg-psw-t").show("fast");
                                      $('.rg-psw input').focus();
                                      return false;
                            }
                            if($(".rg-agreement-checkbox").hasClass("rg-agreement-checkbox")){
                                      //$(".rg-agreement").animate({left:"124px"},300).animate({left:"4px"},200).animate({left:"20px"},50).animate({left:"12px"},50);
                                      return false;
                            }  
                            $("#yoez_submit").fadeOut(200);
                            $("#loading").show();
                            
                },
                error: function(jq,data,errorThrow){
                    $("#loading").hide();
                    $("#yoez_submit").fadeIn(200);
                    alert(data);         
                },
                success: function(html) {
                    if(html.length>0){
                        $("body").html(html);
                        $("body").show();
                    }
                }
              })
              $(".rg-email input").change(function(){
              	    var val=$(".rg-email input").val();
                    var eml=new RegExp("^([-+._]|[a-zA-Z0-9])+@([a-zA-Z0-9])+\.([a-zA-Z])+$");
                    var check=eml.test(val);
                    if(check){
                       var _xrsf=document.cookie.match("\\b_xsrf=([^;]*)\\b");
                       if(_xrsf) _xrsf=_xrsf[1];
                       else _xrsf=undefind;
                       var settings={
                             url:"/user/action/confirm",
                             type:"POST",
                             dataType:"text",
                             data:({user_d:val,
                                    type:"email",
                                    _xsrf:_xrsf}),
                             success:function(html){
                                        if(html=="该邮箱已注册，请换一个!"){
                                             $(".rg-email-t").html(html);
                                             $(".rg-email-t").show("fast");
                                        }
                                        else{
                                             $(".rg-email-t").html('');
                                             $(".rg-email-t").addClass("rg-text-right");
                                             $(".rg-email-t").show("fast");
                                             submite=true;
                                        }
                                  }
                       }
                       $.ajax(settings);
                       }
                    else{
                       $(".rg-email-t").html('这不是一个邮箱');
		       $(".rg-email-t").removeClass("rg-text").addClass("rg-text-warning");
    		       $(".rg-email-t").show("fast");
    		    }
              })
              $(".rg-nic input").change(function(){
                    var _xrsf=document.cookie.match("\\b_xsrf=([^;]*)\\b");
                    if(_xrsf) _xrsf=_xrsf[1];
                    else _xrsf=undefind;
                    var name=$(this).val();
                    var len=name.length;
                    if(len > DEFNAMELEN){
                        $(".rg-nic-t").removeClass("rg-text-right").addClass("rg-text-warning").text("昵称不超过8个字");
                        return;
                    }
                    var settings={
                          url:"/user/action/confirm",
                          type:"POST",
                          dataType:"text",
                          data:({user_d:name,
                                 type:"account",
                                _xsrf:_xrsf}),
                          success:function(html){
                                  if(html=="该用户名已存在，请换一个!"){
                                      $(".rg-nic-t").html(html);
                                      $(".rg-nic-t").show("fast");;
                                  }
                                  else{
                                      submitu=true;
                                      $(".rg-nic-t").html('');
                                      $(".rg-nic-t").addClass("rg-text-right");
                                      $(".rg-nic-t").show("fast");
                                  }
                          }
                    }
                    $.ajax(settings);
                     
              })
              $(".rg-psw input").blur(function(){
              	     var val=$(this).val();
                    if(val.length==0){
                          $(".rg-psw-t").removeClass("rg-text-warning");
                          $(".rg-psw-t").html('密码不要少于6位');
                          $(".rg-psw-t").show("fast");
                    }
                    else if(val.length<6){
                          $(".rg-psw-t").removeClass("rg-text-warning");
                          $(".rg-psw-t").html('密码多于6位比较安全');
                          $(".rg-psw-t").show("fast");
                    }
                    else if(val!=$(".rg-rep input").val()&&$(".rg-rep input").val()){
                          $(".rg-rep-t").addClass("rg-text-warning");
			  $(".rg-rep-t").html('两次输入的密码必须相同');
			  $(".rg-rep-t").show("fast");
                    }
                    else{
                          $(".rg-psw-t").html('');
                          $(".rg-psw-t").addClass('rg-text-right');
			  $(".rg-psw-t").show("fast");
                          submitp=true;
                    }
              })
              $(".rg-rep input").blur(function(){
              	    var val=$(this).val();
                    if(val.length==0){
                          $(".rg-rep-t").removeClass("rg-text-warning");
                          $(".rg-rep-t").html('请再确认一次密码');
                          $(".rg-rep-t").show("fast");
                    }
                    else if($(".rg-psw input").val()!=val){
                          $(".rg-rep-t").addClass("rg-text-warning");
			  $(".rg-rep-t").html('两次输入的密码必须相同');
			  $(".rg-rep-t").show("fast");
                    }
                    else{
                          $(".rg-rep-t").html('');
                          $(".rg-rep-t").addClass("rg-text-right");
			  $(".rg-rep-t").show("fast");
                          submitp=true;
                    }
              })
              $('.rg-agreement span').click(function(){
	            if($(this).hasClass("rg-agreement-checked"))  $(this).removeClass("rg-agreement-checked").addClass("rg-agreement-checkbox");
		    else $(this).removeClass("rg-agreement-checkbox").addClass("rg-agreement-checked");
              })
})
