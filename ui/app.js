// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function buildcard(stripperid, status, switchvalue, instance) {
  if (status == 'True') {
    val_status = 'ONLINE'
    color = 'green'
    btncolor = ''
    cursor = 'pointer'
    disable = ''
  } else {
    val_status = 'OFFLINE'
    color = 'red'
    btncolor = 'gray'
    cursor = 'default'
    disable = 'disabled'
  }
    return "<div class=\"card\" id=\""+instance+"\">"+
            "<span><form id='deletestripper' method=\"post\" onclick=\"\" action=\"/strippers/remove_"+stripperid+"\"><div style=\"cursor:pointer\" type=\"button\"><i class=\"fa fa-trash-o\"></i></div></form></span>"+
            "<img class=\"card-img-top\" src=\"/static/styles/img/stripper.png\" alt=\"Card image cap\">"+
            "<div class=\"card-block\">"+
                "<h4 class=\"card-title\"><b id=\"stripid\">"+stripperid+"<b></h4>"+
                "<p class=\"card-text\">Status:&nbsp<p id=\"stripstat\" style=\"color: "+color+"\">"+val_status+"</p></p>"+
                "<a href=\"#\" class=\"schedule-btn\" style=\"color: "+btncolor+"\">"+
                    "<button class=\"schedule-btn-text\" "+disable+">Schedule <i class=\"fa fa-calendar\"></i></button>"+
                "</a>"+
                "<a href=\"#\">"+
                    "<label class=\"switcher\">"+
                        "<input type=\"checkbox\" "+disable+">"+
                        "<div class=\"slide round\" style=\"cursor: "+cursor+"\"></div>"+
                    "</label>"+
                "</a>"+
            "</div>"+
        "</div>"
}

function loadstrippers() {
  $.ajax({
    url: "/strippers/tasks",
    type:"GET",
    dataType: "json",
    success: function(resp) {
      $("#create").html("");
      if (resp.status  == 'ok') {
        for (i = 0; i < resp.count; i++) {
          id = resp.entries[i].stripperid;
          status = resp.entries[i].status;
          switchvalue = resp.entries[i].switchvalue;
          $("#create").append(buildcard(id, status, switchvalue, i+1));
        }
      } else {   
        $("#create").html("");
        alert(resp.message);
      }
    },
    error: function (e) {
      $("#create").html("You don't have a S-tripper!");
    }
  });
}

//DELETE Stripper Function
$("#create").on("click", "#deletestripper", function(event) {
  url = $(this).attr('action');
  id = $(this).closest("div").attr('id');
  document.getElementById(id).outerHTML="";
  $.ajax({
    url: url,
    type:"POST",
    dataType: "json",
    success: function(resp) {
      if (resp.status  == 'ok') {
        //do nothing
      } else {
        alert("Error!");
      }
    },
    error: function (e) {
      alert("Database Error!");
    }
  });
});

//CREATE Stripper Function
$("#create").on("click", "#regbtn", function(event) {
  url = $(this).attr('action');
  $.ajax({
    url: url,
    type:"POST",
    dataType: "json",
    success: function(resp) {
      if(resp.status == 'ok') {
        alert("Success!");
      } else if (resp.status == 'has owner') {
        alert("Unsuccessful! The device has already an owner!");
      } else {
        alert("Wrong Passcode!");
      }
    },
    error: function (e) {
      alert("Database Error!");
    }
  });
});

//function for f
$(function() {
  var jfk = $(".jfk-bubble"); 
  $("#floatbtn").hover(function() {
    jfk.addClass("active");
  }).blur(function() {
    fk.removeClass("active");
  });
});