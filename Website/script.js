openSocket = () => {
    socketvideo = new WebSocket("ws://192.168.86.249:9997/");
    socketdata = new WebSocket("ws://192.168.86.249:9998/");

    let Values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12]; //Sample Values for the moment

    let msgvideo = document.getElementById("msg");
    //let Value1 = document.getElementById("Value1");

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
        const Array = event.data.split(" ");

        if (Array[0] == "Value1") {
            Values[0] = Array[1];
            document.getElementById("Value1").innerHTML = Values[0];
        }
        else if (Array[0] == "Value2") {
            Values[1] = Array[1];
            document.getElementById("Value2").innerHTML = Values[1];
        }
        else if (Array[0] == "Value3") {
            Values[2] = Array[1];
            document.getElementById("Value3").innerHTML = Values[2];
        }
        else if (Array[0] == "Value4") {
            Values[3] = Array[1];
            document.getElementById("Value4").innerHTML = Values[3];
        }
        else if (Array[0] == "Value5") {
            Values[4] = Array[1];
            document.getElementById("Value5").innerHTML = Values[4];
        }
        else if (Array[0] == "Value6") {
            Values[5] = Array[1];
            document.getElementById("Value6").innerHTML = Values[5];
        }
        else if (Array[0] == "Value7") {
            Values[6] = Array[1];
            document.getElementById("Value7").innerHTML = Values[6];
        }
        else if (Array[0] == "Value8") {
            Values[7] = Array[1];
            document.getElementById("Value8").innerHTML = Values[7];
        }
        else if (Array[0] == "Value9") {
            Values[8] = Array[1];
            document.getElementById("Value9").innerHTML = Values[8];
        }
        else if (Array[0] == "Value10") {
            Values[9] = Array[1];
            document.getElementById("Value10").innerHTML = Values[9];
        }
    });
}