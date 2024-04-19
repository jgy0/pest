
function f() {
    $("#captcha-btn").click(function (event) {
        let $this=$(this)
        // 阻止默认的事件
        event.preventDefault();

       let email = $("input[name='email']").val();
       $.ajax({
           url:"/auth/captcha/email?email="+email,
           method:"GET",
           success:function (result){
               let code=result['code']
               if(code==200){
                   let countdown=60
                   $this.off("click");
                   // 取消点击事件
                   let timer = setInterval(function () {
                       $this.text(countdown)
                       countdown-=1;
                       if(countdown<=0)
                       {
                            clearInterval(timer);
                            $this.text("获取验证码")
                           // 重新绑定点击事件
                            f();
                       }
                   },1000)
                   alert('邮件发送成功')
               }else
               {
                   alert(result['message'])
               }
           },
           fail:function (error) {
               console.log(error)
           }
       })
    });

}


$(function () {
    f();
})
