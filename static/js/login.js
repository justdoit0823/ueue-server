$(document).ready(function(){
    $(".inputtipdiv input").each(function(){
        if($(this).val())  $(this).next().hide();
        else $(this).next().show();
    })
    $(".inputtipdiv span").click(function(){
        $(this).hide();
        $(this).prev().focus();
    })
    $(".inputtipdiv input").focus(function(){
        $(this).next().hide();
    })
    $(".inputtipdiv input").blur(function(){
        if(!$(this).val()){
            $(this).next().show();
        }
    })
              $("#yoez_submit").attr('disabled','');
              $("#yoez_login_f").ajaxForm({
              	  dataType:'json',
                beforeSubmit: function(a,f,o) {
		            if($("input[name='email']").val().length == 0){
			            //$(".rg-text").show("fast");
                                    $("input[name='email']").focus();
			            return false;
		            }
		            if($("input[name='password']").val().length == 0){
			            //$(".rg-text-warning").show("fast");
                                    $("input[name='password']").focus();
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
                success: function(result) {
                    if(result.error){
                        $("#loading").hide();
                        $("#yoez_submit").fadeIn(200);
                        $(".log-text-warning").html(result.msg);
                        $(".log-warning").show();
                    }
                    else location.href=result.url;
                }
              });
})
