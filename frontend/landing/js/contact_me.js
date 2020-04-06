$(function() {
  const { scheme, hostname } =
    process.env.NODE_ENV === "production"
      ? { scheme: "https"
        , hostname: window.location.hostname }
      : { scheme: "http"
        , hostname: "localhost:"+window.location.port };

  $("#registerForm input").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      const dataSerialized = $("#registerForm").serializeArray();
      const data = dataSerialized.reduce((obj, elem) => {
        obj[elem.name] = elem.value;
        return obj;
      }, {});
      const languageEl = document.getElementById("language");
      const languageStr = languageEl.options[languageEl.selectedIndex].value;
      data["language"] = languageStr;
      $this = $("#registerAccount");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages

      function onSucess(msgs) {
        // Success message
        $('#success').html("<div class='alert alert-success'>");
        $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
          .append("</button>");
        $('#success > .alert-success')
          .append(`<strong>${msgs["createdCoopSuccessMsg"]}</strong><br/>${msgs["accountNeedsToBeActivatedMsg"]}`);
        $('#success > .alert-success')
          .append('</div>');
        //clear all fields
        $('#registerForm').trigger("reset");
      }

      function onError(err) {
        let message = "";
        if (err.status === 400) {
          if (Object.keys(err.responseJSON).length) {
            message = Object.values(err.responseJSON).flat().join('<br>');
          } else {
            message = "There has been an error. Check your data.";
          }
        } else {
          message = "There has been an error. Please try again later.";
        }
        // Fail message
        $('#success').html("<div class='alert alert-danger'>");
        $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
          .append("</button>");
        $('#success > .alert-danger').append($("<strong>")
          .html(message));
        $('#success > .alert-danger').append('</div>');

        //clear all fields
        // $('#registerForm').trigger("reset");
      }

      function onComplete() {
        setTimeout(function() {
          $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
        }, 1000);
      }

      grecaptcha.ready(() => {
        grecaptcha.execute('6LepzsgUAAAAAJTtaoDibT1Duf2CFQrI0RFl3srT', {action: 'signup'})
          .then((reCaptchaToken) => {
            data.reCaptchaToken = reCaptchaToken;
            $.ajax({
              url: `${scheme}://${hostname}/api/cooperatives/`,
              type: "POST",
              headers: {"Accept-Language": $('#language').val() || 'en'},
              data,
              cache: false,
              success: (msgs) => {onSucess(msgs)},
              error: (err) => {onError(err)},
              complete: onComplete
            });
          })
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});
