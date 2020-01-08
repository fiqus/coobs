/*
* This example shows that you can:
* - change the language on the fly.
*/
var myDictionary = {
  en: {
    "signIn": "Sign in",
    "welcomeToCoobs": "Welcome to COOBS!",
    "subtitle": "This is the best site around the world to manage your actions and build the cooperative balance.",
    "joinUs": "Join us!",
    "coopBusinessName": "Cooperative business name",
    "enterCoopName": "Please enter the cooperative business name.",
    "firstName": "First name",
    "lastName": "Last name",
    "email": "Email address",
    "enterEmail": "Please enter your email address.",
    "password": "Password",
    "minLengthPass": "Minimum 8 characters.",
    "lettersAndNumbers": "Must contain letters and numbers.",
    "required": "Required",
    "repeatPassword": "Repeat password",
    "passwordNotMatch": "Passwords must match.",
    "goodPasswordHelpText": "Password must be more than 8 characters long, contain letters and numbers.",
    "COOPERATIVE_ALREADY_EXISTS": "The cooperative entered already exists.",
    "EMAIL_ALREADY_EXISTS": "Already exists an user with the same email entered.",
    "INVALID_RECAPTCHA": "There was an error validation the interntal captcha. Try again later.",
    "registerAccount": "Register account",
    "alreadyHaveAccount": "Already have an account? Login!",
    "whyToJoin": "Why to join COOBS?",
    "aboutCoobs": `The Co-operative Social Balance (COOP + BS = COOBS) is a methodology developed 
      by the International Co-operative Alliance, whose objective is to become a tool for socio-economic 
      management that makes it easier for co-operatives to measure themselves and be accountable to their 
      members, in their capacity as owners, managers, users and all other stakeholders who are impacted by 
      their actions in relation to the fulfilment of their own essence or identity, i.e. 
      from the perspective of co-operative values and principles.`,
      "registerNow": "Register now!",
      "aboutFiqusLabs": "Developed at FiqusLabs, a space where we create open source technology oriented to the community."
  },
  es : {
    "signIn": "Inicie sesión",
    "welcomeToCoobs": "Bienvenido a COOBS!",
    "subtitle": "Este es el mejor sitio del mundo para administrar sus acciones cooperativas y construir el balance de su organización.",
    "joinUs": "Únete a nosotros!",
    "coopBusinessName": "Razón social de la Cooperativa",
    "enterCoopName": "Ingrese la razón social de la Cooperativa.",
    "firstName": "Nombre",
    "lastName": "Apellido",
    "email": "Email",
    "enterEmail": "Ingrese su email.",
    "password": "Contraseña",
    "minLengthPass": "Mínimo 8 caracteres.",
    "passwordNotMatch": "Las contraseñas deben coincidir.",
    "goodPasswordHelpText": "La contraseña debe tener mínimo ocho caracteres, al menos una letra y un número.",
    "lettersAndNumbers": "Debe contener letras y números.",
    "required": "Obligatorio",
    "repeatPassword": "Repita la constraseña",
    "COOPERATIVE_ALREADY_EXISTS": "La cooperativa ingresada ya existe.",
    "EMAIL_ALREADY_EXISTS": "Ya existe un usuario con el mismo mail ingresado.",
    "INVALID_RECAPTCHA": "Hubo un error al validar el captcha internamente. Pruebe más tarde.",
    "registerAccount": "Registrar cuenta",
    "alreadyHaveAccount": "Ya tenés una cuenta? Ingresa!",
    "whyToJoin": "Por qué unirse a COOBS?",
    "aboutCoobs": `El Balance Social Cooperativo (COOP + BS = COOBS) es una metodología desarrollada 
      por la Alianza Internacional de Cooperativas, cuyo objetivo es convertirse en una herramienta de 
      gestión socioeconómica que facilite a las cooperativas la medición de sí mismas y la rendición 
      de cuentas a sus socios, en su calidad de propietarios, gestores, usuarios y todos los demás 
      interesados que se ven afectados por sus acciones en relación con el cumplimiento de su propia 
      esencia o identidad, es decir, desde la perspectiva de los valores y principios cooperativos.`,
    "registerNow": "Registrate ahora!",
    "aboutFiqusLabs": "Desarrollado en FiqusLabs, un espacio donde creamos tecnología de código abierto orientada a la comunidad."
  }
}
$.tr.dictionary(myDictionary);
$(document).ready(function() {

  // change the language
  $('#language').change(function() {
    $.tr.language($(this).val());
    var tr = $.tr.translator();
    Object.keys(myDictionary["en"]).forEach((key) => {
      $('#' + key).text(tr(key));
    })
    $("#coopBusinessName").attr('placeholder', tr("coopBusinessName"));
    $("#firstName").attr('placeholder', tr("firstName"));
    $("#lastName").attr('placeholder', tr("lastName"));
    $("#email").attr('placeholder', tr("email"));
    $("#password").attr('placeholder', tr("password"));
    $("#repeatPassword").attr('placeholder', tr("repeatPassword"));
  });

  var language = $.tr.language('es', true);

  $('#language').val(language);
  $('#language').change();
});