openSocket = () => {

    socketvideo = new WebSocket("ws://127.0.0.1:9997/");
    socketdata = new WebSocket("ws://127.0.0.1:9998/");

    let msgvideo = document.getElementById("msg");
    let Value1 = document.getElementById("Value1");

    // Video Socket Opened
    socketvideo.addEventListener('open', (e) => {
        document.getElementById("status").innerHTML = "Opened";
    });

    // Video Socket Data Pass
    socketvideo.addEventListener('message', (e) => {
        let ctx = msgvideo.getContext("2d");
        let image = new Image();
        image.src = URL.createObjectURL(e.data);
        image.addEventListener("load", (e) => {
            ctx.drawImage(image, 0, 0, msgvideo.width, msgvideo.height);
        });
    });

    // Data Socket Opened
    socketdata.addEventListener('open', (e) => {
        document.getElementById("status2").innerHTML = "Opened";
    });

    // Data Socket Value Pass
    /*
    socketdata.addEventListener('message', (e) => {
        document.getElementById("Value1").innerHTML = Value1.getContext();
    });
    */
    socketdata.addEventListener('message', function (event) {
        //console.log(event.data);
        document.getElementById("Value1").innerHTML = event.data;
    });
}
