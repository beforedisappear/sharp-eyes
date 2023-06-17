function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
         const cookie = cookies[i].trim();
         // Does this cookie string begin with the name we want?
         if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
         }
      }
   }
   return cookieValue;
}

$(function ($){
   $('#authform, #regform, #resetform, #progressform').submit(function (e) {
      e.preventDefault();
      var form = e.target.id;
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            if ((form === "regform" ) || ((form === "resetform" ))|| ((form === "progressform" ))) {
               console.log(response.success);
            } else if (e.target.id === "authform"){
               window.location.href = response.success;
            }
         },
         error: function (response) {
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            for (const [key, value] of Object.entries(data.errors)) {
               if ((jQuery.type(value) === "object") && ((form != "resetform"))) {
                  for (const [k, v] of Object.entries(value)){
                     console.log(v);
                  }
               } else {
                  console.log(value);
               }
            }
         }
      })
   })
})


$(function ($){
   var initdataname = $("#useredit input[type=text][name=username]").serialize();
   $('#useredit, #resetpassword').submit(function (e) {
      e.preventDefault();
      var form = e.target.id;
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            console.log(response.success);
            if (form === "useredit") {
               var name = e.target.username.value;
               var curdataname = $("#useredit input[type=text][name=username]").serialize();
               if (curdataname != initdataname) {
                  var newurl = this.url.split('-')[0] + '-' + name.toLowerCase() + '/';
                  window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", newurl);
               }
            }

         },
         error: function (response) {
            if (form === "resetpassword") {
               alert("Непредвиденная ошибка");
               return;
            }
            
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            for (const [key, value] of Object.entries(data.errors)) {
               if (jQuery.type(value) === "object") {
                  for (const [k, v] of Object.entries(value)){
                     console.log(v);
                  }
               } else {
                  console.log(value);
               }
            }
         }
      })
   })
})