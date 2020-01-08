$(function() {

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
      $this = $("#registerAccount");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages

      function onSucess() {
        // Success message
        $('#success').html("<div class='alert alert-success'>");
        $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
          .append("</button>");
        $('#success > .alert-success')
          .append(`<strong>The cooperative ${data.businessName} has been created for user ${data.firstName} ${data.lastName} with email ${data.email}.</strong>`);
        $('#success > .alert-success')
          .append('</div>');
        //clear all fields
        $('#registerForm').trigger("reset");
      }

      function onError(err) {
        let message = "";
        let hasErrorCode = false;
        if (err.status === 400) {
          if (err.responseJSON.ERROR_CODE) {
            message = err.responseJSON.ERROR_CODE;
            hasErrorCode = true;
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
        $('#success > .alert-danger').append($(`<strong id="${message}">`)
          .text(message));
        $('#success > .alert-danger').append('</div>');

        if (hasErrorCode) {
          // translate current error
          var tr = $.tr.translator();
          $(`#${message}`).text(tr(message));
        }
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
              url: "http://127.0.0.1:8000/api/cooperatives/", // TODO fix URL
              type: "POST",
              data,
              cache: false,
              success: onSucess,
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
