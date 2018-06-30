$(function () {
    var error_name = true;
    var error_pwd = true;
    var error_yzm = true;



    $('.verificationcode1').click(function () {

        change_yzm();
    });



    $('.verificationcode').blur(function () {

        check_yam();

    });

    $('.name_input').blur(function () {
        check_username();
    });

    //更换验证码
    function change_yzm() {
        var url='/user/verificationcode?d=';
        alert($('.verificationcode1').attr('src'));
        $('.verificationcode1').attr('src',url+new Date().getTime());
    }

    //验证验证码
    function check_yam() {
        var user_yzm=$('.verificationcode').val();

        $.ajax({
            'url':'/user/check_yzm',
            'type':'get',
            'data':'yzm='+user_yzm,
            'success':function (date) {
                if (date=='1'){
                    $('.yzm_error').html('验证码错误');
                    $('.yzm_error').show();
                    error_yzm = true;
                }
                else {
                    $('.yzm_error').hide();
                    error_yzm = false;
                }
            }
        }
        )
    }

    //验证用户名是否存在
    function check_username() {
        username = $('.name_input').val();
        $.ajax({
            'type': 'get',
            'url': '/user/check_user_name',
            'data': 'uname=' + username,
            'success': function (date) {

                if (date == '0') {
                    $('.name_input').next().html('用户名不存在')
                    $('.name_input').next().show();
                    error_name = true;
                }
                else {
                    $('.pass_input').blur(function () {
                        check_pwd();
                    });
                    $('.name_input').next().hide();
                    error_name = false;
                }
            }
        });
    }

    //验证密码
    function check_pwd() {
        username = $('.name_input').val();
        pwd = $('.pass_input').val();
        $.ajax({
            'type': 'get',
            'url': '/user/check_user_pwd',
            'data': 'uname=' + username + '&&pwd=' + pwd,
            'success': function (date) {

                if (date == '0') {
                    $('.pass_input').next().html('密码错误')
                    $('.pass_input').next().show();
                    error_pwd = true;
                }
                else {
                    $('.pass_input').next().hide();
                    error_pwd = false;
                }
            }
        });
    }





    $('#login_form').submit(function () {
        check_username();
        check_pwd();

        if (error_name == false && error_pwd == false && error_yzm == false) {
            return true;
        }
        else {
            return false;
        }

    });
});
