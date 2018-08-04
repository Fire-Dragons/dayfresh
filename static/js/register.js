$(function () {

    var error_name = false;
    var error_password = false;
    var error_check_password = false;
    var error_email = false;
    var error_check = false;
    var error_eyzm = false;


    $('#user_name').blur(function () {
        check_user_name();
    });

    $('#pwd').blur(function () {
        check_pwd();
    });

    $('#cpwd').blur(function () {
        check_cpwd();
    });

    $('#email').blur(function () {
        check_email();
    });

    $('#eyzm').blur(function () {
        check_eyzm();
    });

    //邮箱验证倒计时
    $('.i-txt-get-code').one('click', function () {
        //发送邮件
        send_mail();
    });

    function send_mail() {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();
        if (error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false) {
            //倒计时
            countdown();
            $('.i-txt-get-code').next().hide();
            username = $('#user_name').val();
            email = $('#email').val();
            upasswd = $('#pwd').val();
            $.ajax(
                {
                    'type': 'get',
                    'url': '/user/send_email',
                    'datatype': 'json',
                    'data': {'uname': username, 'umail': email, 'upasswd': upasswd},
                    'success': function (date) {

                        if (date == '0') {
                            alert('邮件发送失败')
                        }

                    }
                }
            );

        } else {
            $('.i-txt-get-code').next().show();
            $('.i-txt-get-code').next().html('请先输入上面的信息');
        }

    }


    //倒计时
    var time = 60;

    function countdown() {
        if (time == 0) {
            //e.setAttribute('disabled',false);         对没有disbaled属性的span标签，此方法无效
            // $('.i-txt-get-code').setAttribute("onclick","send_mail(this)");
            $('.i-txt-get-code').html("获取验证码");

            time = 60;
            //邮箱验证倒计时
            $('.i-txt-get-code').one('click', function () {
                //发送邮件
                send_mail();
            });
        } else {
            //e.attr('disabled',true);                  对没有disbaled属性的span标签，此方法也无效
            //e.setAttribute("onclick", '');            这样写也可以
            // $('.i-txt-get-code').removeAttr("onclick");
            $('.i-txt-get-code').html("重新发送(" + time + ")");
            time--;
            setTimeout(function () {
                countdown();
            }, 1000)


        }

    }


    $('#allow').click(function () {
        if ($(this).is(':checked')) {
            error_check = false;
            $(this).siblings('span').hide();
        }
        else {
            error_check = true;
            $(this).siblings('span').html('请勾选同意');
            $(this).siblings('span').show();
        }
    });


    function check_user_name() {
        var username = $('#user_name').val();
        var myReg = /^[a-zA-Z0-9_]{5,20}$/;
        if (!myReg.test(username)) {

            $('#user_name').next().html('请输入5-20个字符的用户名')
            $('#user_name').next().show();
            error_name = true;
        }
        else {
            $.ajax({
                'type': 'get',
                'url': '/user/check_user_name',
                'data': 'uname=' + username,
                'success': function (date) {
                    if (date == '1') {
                        $('#user_name').next().html('用户名已注册')
                        $('#user_name').next().show();
                        error_name = true;
                    }
                    else {
                        $('#user_name').next().hide();
                        error_name = false;
                    }
                }
            });

        }
    }

    function check_pwd() {
        var len = $('#pwd').val().length;
        if (len < 8 || len > 20) {
            $('#pwd').next().html('密码最少8位，最长20位')
            $('#pwd').next().show();
            error_password = true;
        }
        else {
            $('#pwd').next().hide();
            error_password = false;
        }
    }


    function check_cpwd() {
        var pass = $('#pwd').val();
        var cpass = $('#cpwd').val();

        if (pass != cpass) {
            $('#cpwd').next().html('两次输入的密码不一致')
            $('#cpwd').next().show();
            error_check_password = true;
        }
        else {
            $('#cpwd').next().hide();
            error_check_password = false;
        }

    }

    function check_email() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if (re.test($('#email').val())) {
            $('#email').next().hide();
            error_email = false;
        }
        else {
            $('#email').next().html('你输入的邮箱格式不正确')
            $('#email').next().show();
            error_check_password = true;
        }

    }


    //验证邮箱验证码
    function check_eyzm() {
        var user_eyzm = $('#eyzm').val();
        if (user_eyzm == '') {
            error_eyzm = true;
            $('.i-txt-get-code').next().html('邮箱验证码为空');
            $('.i-txt-get-code').next().show();
        }
        else {
            $.ajax({
                    'url': '/user/activate/',
                    'type': 'get',
                    'data': 'ueyzm=' + user_eyzm,
                    'success': function (date) {
                        if (date == '1') {
                            $('.i-txt-get-code').next().hide();
                            error_eyzm = false;
                        }
                        else {
                            $('.i-txt-get-code').next().html('邮箱验证码错误');
                            $('.i-txt-get-code').next().show();
                            error_eyzm = true;
                        }
                    }
                }
            )
        }
    }

    $('#reg_form').submit(function () {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();
        check_eyzm();
        if (error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false && error_eyzm == false) {
            return true;
        }
        else {
            return false;
        }

    });


});
