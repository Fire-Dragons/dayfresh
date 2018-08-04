$(function () {

    var error_rece = false;
    var error_addr = false;
    var error_phone = false;
    var error_code = false;

    $(".hovertable td").mouseover(function (event) {
        event.target.parentNode.setAttribute('class', 'showdiv')
    });
    $(".hovertable td a").mouseover(function (event) {
        event.target.parentNode.parentNode.setAttribute('class', 'showdiv')
    });
    $(".hovertable td").mouseout(function (event) {
        event.target.parentNode.removeAttribute('class')
    });
    $(".hovertable td a").mouseout(function (event) {
        event.target.parentNode.parentNode.removeAttribute('class')
    });

    $('#receiver').blur(function () {
        check_rece();
    });

    $('#addr').blur(function () {
        check_addr();
    });

    $('#zip_code').blur(function () {
        check_code();
    });

    $('#phone').blur(function () {
        check_phone();
    });

    function check_rece() {
        var receiver = $('#receiver').val();
        if (receiver == '') {
            $('#receiver').next().html('收件人不能为空')
            $('#receiver').next().show();
            error_rece = true;
        }
        else {
            $('#receiver').next().hide();
            error_rece = false
        }
    }

    function check_addr() {
        var addr = $('#addr').val();
        if (addr == '') {
            $('#addr').next().html('地址不能为空')
            $('#addr').next().show();
            error_addr = true;
        }
        else {
            $('#addr').next().hide();
            error_addr = false
        }
    }

    function check_code() {
        var zip_code = $('#zip_code').val();
        var myReg = /^[0-9]{6}$/;
        if (!myReg.test(zip_code)) {
            $('#zip_code').next().html('邮编输入错误')
            $('#zip_code').next().show();
            error_code = true;
        }
        else {
            $('#zip_code').next().hide();
            error_code = false
        }
    }


    function check_phone() {
        var re = /^(13\d|14[5|9]|15[0|1|2|5|6|7|8|9]|17[1|3|5|6|7|8]|18\d)\d{8}$/;

        if (re.test($('#phone').val())) {
            $('#phone').next().hide();
            error_phone = false;
        }
        else {
            $('#phone').next().html('你输入的手机号格式不正确')
            $('#phone').next().show();
            error_phone = true;
        }

    }

    $('#add_form').submit(function () {
        check_rece();
        check_addr();
        check_code();
        check_phone();

        if (error_rece == false && error_addr == false && error_phone == false && error_code == false) {
            return true;
        }
        else {
            return false;
        }

    });

});
