window.addEventListener("DOMContentLoaded", () => {
  const formOpenBtn = document.querySelector("#form-open"),
    home = document.querySelector(".home"),
    // formContainerLog = document.querySelector(".form_container_log"),
    // formContainerReg = document.querySelector(".form_container_reg"),
    formCloseBtnLog = document.querySelector(".form_close_log"),
    formCloseBtnReg = document.querySelector(".form_close_reg"),
    formCloseBtnRec = document.querySelector(".form_close_rec"),
    signupBtn = document.querySelector("#signup"),
    loginBtn = document.querySelector("#login"),
    recoverBtn = document.querySelector("#recover"),
    formOpenLog = document.querySelector("#form-open-log"),
    formOpenReg = document.querySelector("#form-open-reg"),
    pwShowHide = document.querySelectorAll(".pw_hide");

  // formOpenBtn?.addEventListener("click");
  formOpenBtn?.addEventListener("click", (e) => onShowRegPopup(e));
  formOpenLog?.addEventListener("click", (e) => onShowLogPopup(e));
  formOpenReg?.addEventListener("click", (e) => onShowRegPopup(e));
  formCloseBtnLog?.addEventListener("click", (e) => onHideLogPopup(e));
  formCloseBtnReg?.addEventListener("click", (e) => onHideRegPopup(e));
  formCloseBtnRec?.addEventListener("click", (e) => onHideResetPopup(e));

  const onShowLogPopup = (e) => {
    home.classList.add("show_log");
  };

  const onShowRegPopup = (e) => {
    home.classList.add("show_reg");
  };

  const onShowResetPopup = (e) => {
    home.classList.add("show_rec");
  };

  const onHideResetPopup = (e) => {
    home.classList.remove("show_rec");
  };

  const onHideLogPopup = (e) => {
    home.classList.remove("show_log");
  };

  const onHideRegPopup = (e) => {
    home.classList.remove("show_reg");
  };

  pwShowHide.forEach((icon) => {
    icon.addEventListener("click", () => {
      let getPwInput = icon.parentElement.querySelector("input");
      if (getPwInput.type === "password") {
        getPwInput.type = "text";
        icon.classList.replace("uil-eye-slash", "uil-eye");
      } else {
        getPwInput.type = "password";
        icon.classList.replace("uil-eye", "uil-eye-slash");
      }
    });
  });

  signupBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    home.classList.remove("show_log");
    home.classList.add("show_reg");
  });

  loginBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    home.classList.add("show_log");
    home.classList.remove("show_reg");
  });

  recoverBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    home.classList.remove("show_log");
    home.classList.add("show_rec");
  });

  const succesfullRegistataion = document.querySelector(
    "succesfull_registataion"
  );

  if (succesfullRegistataion) console.log(succesfullRegistataion);

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  $(function ($) {
    $("#authform, #regform, #resetform, #progressform").submit(function (e) {
      e.preventDefault();
      var form = e.target.id;
      $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        dataType: "json",
        success: function (response) {
          if (form === "resetform" || form === "progressform") {
            console.log(response.success);
            alert(response.success);

            if (form === "resetform") {
              document.getElementById("resetform").reset();
            }
          } else if (form === "regform") {
            console.log(response.success);
            alert(response.success);
            document.getElementById("regform").reset();
            onHideRegPopup();
          } else if (form === "authform") {
            window.location.href = response.success;
          }
        },
        error: function (response) {
          var data = JSON.parse(JSON.stringify(response["responseJSON"]));
          for (const [key, value] of Object.entries(data.errors)) {
            if (jQuery.type(value) === "object" && form != "resetform") {
              for (const [k, v] of Object.entries(value)) {
                alert(v);
              }
            } else {
              alert(value);
            }
          }
        },
      });
    });
  });

  $(function ($) {
    var initdataname = $(
      "#useredit input[type=text][name=username]"
    ).serialize();
    $("#useredit, #resetpassword").submit(function (e) {
      e.preventDefault();
      var form = e.target.id;
      $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        dataType: "json",
        success: function (response) {
          console.log(response.success);
          alert(response.success);
          if (form === "useredit") {
            var name = e.target.username.value;
            var curdataname = $(
              "#useredit input[type=text][name=username]"
            ).serialize();
            if (curdataname != initdataname) {
              var newurl =
                this.url.split("-")[0] + "-" + name.toLowerCase() + "/";
              window.history.pushState(
                { html: response.html, pageTitle: response.pageTitle },
                "",
                newurl
              );
            }
          }
        },
        error: function (response) {
          if (form === "resetpassword") {
            alert("Непредвиденная ошибка");
            return;
          }

          var data = JSON.parse(JSON.stringify(response["responseJSON"]));
          for (const [key, value] of Object.entries(data.errors)) {
            if (jQuery.type(value) === "object") {
              for (const [k, v] of Object.entries(value)) {
                console.log(v);
                alert(v);
              }
            } else {
              console.log(value);
              alert(value);
            }
          }
        },
      });
    });
  });
});
