<<<<<<< Updated upstream
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

// template
// $(function ($){
//    $('#resetform').submit(function (e) {
//       e.preventDefault()
//       $.ajax({
//          type: this.method,
//          url: this.action,
//          data: $(this).serialize(),
//          headers: {'X-CSRFToken': getCookie('csrftoken')},
//          dataType: 'json',
//          success: function (response) {
//             console.log('okay', response)
//          },
//          error: function (response) {
//             console.log('err - ', response);
//          }
//       })
//    })
// })

// multiple function
// $(function ($){
//    $('form').submit(function (e) {
//       e.preventDefault()
//       $.ajax({
//          type: this.method,
//          url: this.action,
//          data: $(this).serialize(),
//          headers: {'X-CSRFToken': getCookie('csrftoken')},
//          dataType: 'json',
//          success: function (response) {
//             console.log(response.success)
//             //window.location.href;
//          },
//          error: function (response) {
//             var data = JSON.parse(JSON.stringify(response['responseJSON']));
//             console.log(data);
//             for (const [key, value] of Object.entries(data.errors)) {
//                console.log(value);
//             }
//          }
//       })
//    })
// })


$(function ($){
   $('#authform, #regform, #resetform').submit(function (e) {
      e.preventDefault();
      var form = e.target.id;
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            if ((form === "regform" ) || ((form === "resetform" ))) {
               console.log(response.success);
            } else if (e.target.id === "authform"){
               window.location.href = response.success;
            }
         },
         error: function (response) {
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            for (const [key, value] of Object.entries(data.errors)) {
               if ((jQuery.type(value) === "object") && (form != "resetform")) {
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
      var name = e.target.username.value;
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            console.log(response.success);
            var curdataname = $("#useredit input[type=text][name=username]").serialize();
            if (curdataname != initdataname) {
               var newurl = this.url.split('-')[0] + '-' + name.toLowerCase() + '/';
               window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", newurl);
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
=======
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

// template
// $(function ($){
//    $('#resetform').submit(function (e) {
//       e.preventDefault()
//       $.ajax({
//          type: this.method,
//          url: this.action,
//          data: $(this).serialize(),
//          headers: {'X-CSRFToken': getCookie('csrftoken')},
//          dataType: 'json',
//          success: function (response) {
//             console.log('okay', response)
//          },
//          error: function (response) {
//             console.log('err - ', response);
//          }
//       })
//    })
// })

// multiple function
// $(function ($){
//    $('form').submit(function (e) {
//       e.preventDefault()
//       $.ajax({
//          type: this.method,
//          url: this.action,
//          data: $(this).serialize(),
//          headers: {'X-CSRFToken': getCookie('csrftoken')},
//          dataType: 'json',
//          success: function (response) {
//             console.log(response.success)
//             //window.location.href;
//          },
//          error: function (response) {
//             var data = JSON.parse(JSON.stringify(response['responseJSON']));
//             console.log(data);
//             for (const [key, value] of Object.entries(data.errors)) {
//                console.log(value);
//             }
//          }
//       })
//    })
// })


$(function ($){
   $('#authform, #regform, #resetform').submit(function (e) {
      e.preventDefault();
      var form = e.target.id;
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            if ((form === "regform" ) || ((form === "resetform" ))) {
               console.log(response.success);
            } else if (e.target.id === "authform"){
               window.location.href = response.success;
            }
         },
         error: function (response) {
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            for (const [key, value] of Object.entries(data.errors)) {
               if ((jQuery.type(value) === "object") && (form != "resetform")) {
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
      var name = e.target.username.value;
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            console.log(response.success);
            var curdataname = $("#useredit input[type=text][name=username]").serialize();
            if (curdataname != initdataname) {
               var newurl = this.url.split('-')[0] + '-' + name.toLowerCase() + '/';
               window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", newurl);
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
>>>>>>> Stashed changes
})