/**
 * Created by Administrator on 2017/11/18.
 */
function picMove() {
    var x = event.clientX;
    var y = event.clientY;
    var x_per = (x-960)*2/1920;
    var y_per = (y-540)*4/1080;
    var bg_image = document.getElementById("bg_image");
    bg_image.style.top = y_per - 5 + "%";
    bg_image.style.left  = x_per - 5 + "%";
}