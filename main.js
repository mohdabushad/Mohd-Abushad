$(document).ready(function () {

 
  $(".text").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 640,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    height: 200,
    autostart: true,
    
  });
    $(".siri-message").textillate({
   
  });

  $("#MicBtn").click(function () {
  
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

   
  });


});
