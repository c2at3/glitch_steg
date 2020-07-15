$(document).ready(function() {

    // ẨN TIN
    hideMessage();
    //END ẨN TIN

    //Giải tin
    showMessage();
    //END Giải tin

    $('.Change-Steg').click(function(e) {
        var title = $('.titleFunc').text();
        if (title == "LSB-Steganography: Giấu tin") {
            reset();
            $('textarea').attr('style', 'display:block; width: 65%;');
            $('.changeFunc').removeClass('animationChangeShow');
            $('.changeFunc').addClass('animationChangeHide');
            $('form[name="hideFunc"]').attr('style', 'display:none');
            $('form[name="showFunc"]').attr('style', 'display:block');
            $('.titleFunc').text('LSB-Steganography: Giải mã');
        } else {
            reset();
            $('textarea').attr('style', 'display:none');
            $('textarea').val('');
            $('.changeFunc').removeClass('animationChangeHide');
            $('.changeFunc').addClass('animationChangeShow');
            $('form[name="showFunc"]').attr('style', 'display:none');
            $('form[name="hideFunc"]').attr('style', 'display:block');
            $('.titleFunc').text('LSB-Steganography: Giấu tin');
        }
    });

});

function reset() {
    $('textarea').val('');
    $('.file-image').attr('src', '');
    $('.file-image').attr('alt', '');
    $('.file-image-hide').attr('src', '');
    $('.file-image-hide').attr('alt', '');
    $('.img-up-two').attr('style', 'display:none');
    $('.img-up-one').attr('style', 'display:none');
}

function showMessage() {
    $('#uploadShow').click(function(e) {
        $('#uploadfileShow').click();
    });

    $('#reset').click(function(e) {
        reset();
    });
}

function hideMessage() {
    $('#upload').click(function(e) {
        $('#uploadfile').click();
        addImg();
    });

    $('input[type="reset"]').click(function(e) {
        reset();
    });

}

function getSizeAndCheck(elem) {
    extensions = ['bmp', 'svg', 'tif', 'tiff', 'ico', 'png',
        'jpg', 'jpeg', 'gif', 'pjp', 'pjpeg', 'jfif',
        'svgz', 'xbm', 'dib', 'webp'
    ];
    if (elem.files.length != 0) {
        file = elem.files[0];
        filename = file.name;
        filename = filename.toLowerCase();
        filename = filename.split(".");
        extensionsFile = filename[filename.length - 1];
        if (file.size <= (10 * 1024 * 1024)) {
            if (extensions.indexOf(extensionsFile) != -1) {
                $('.img-up-one').last().attr('style', 'display:block');
                document.cookie = `filesize=${elem.files[0].size}`
            } else {
                alert("Định dạng không được hỗ trợ !");
                $('.img-up-one').last().attr('style', 'display:none');
                $('#uploadfile').val("");
                $('.file-image').last().attr('alt', '');
                $('.file-image').last().attr('src', '');
            }
        } else {
            alert("Kích thước tối đa cho phép là 10MB");
            $('.img-up-one').last().attr('style', 'display:none');
            $('#uploadfile').val("");
            $('.file-image').last().attr('alt', '');
            $('.file-image').last().attr('src', '');
        }
    }
}

function addImg() {
    $('#uploadfile').on('change', function() {
        $('.file-image-hide').attr('src', '');
        $('.file-image-hide').attr('alt', '');
        $('.img-up-two.img1').attr('style', 'display:block');
        $('.img-up-two.img2').attr('style', 'display:none');
        var files = $(this)[0].files;
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            console.log('DEBUG FOR');
            console.log(i, file.name, file.size);
            var fileReader = new FileReader();
            fileReader.onload = function() {
                console.log('DEBUG ONLOAD');
                console.log(file.name, file.size);
                var imageSrc = event.target.result;
                var fileName = file.name;
                var fileSize = file.size;
                $('.file-image').last().attr('alt', fileName);
                $('.file-image').last().attr('src', imageSrc);
            };
            fileReader.readAsDataURL(file);
        }
    });
}