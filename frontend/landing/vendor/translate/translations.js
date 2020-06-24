/*
* This example shows that you can:
* - change the language on the fly.
*/
var langDict = {
  en: {
    "signIn": "Sign in",
    "header-title-1": "COOBS:",
    "header-title-2": "Cooperative Social Balance",
    "header-subtitle": "This is a tool that will help you to monitor all the actions of your social organization, guided by the cooperative principles and the sustainable development goals.",
    "section-metrics-title": "Metrics and monitoring",
    "section-metrics-subtitle": "The tool will provide you with the possibility of monitoring your social activity in real time, being able to measure the incidence of your actions.",
    "section-bs-title": "Organic Social Balance",
    "section-bs-subtitle": "Coobs offers you the possibility to plan future actions to guide the performance of your social organization by following cooperative values.",
    "signup": "Signup",
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
    "section-labs-text": "Developed at FiqusLabs, a space where we create community-oriented open source technology.",
    "firstImageTextTitle": "Load the actions that your cooperative performs",
    "firstImageTextDescription": "In COOBS you can load the actions that your cooperative makes related to each cooperative principle.",
    "secondImageTextTitle": "Watch all your cooperative activity",
    "secondImageTextDescription": "You will be able to see daily what you do in your co-operative related to each co-operative principle allowing you to take action to improve it.",
    "thirdImageTextTitle": "Get your annual balance sheet",
    "thirdImageTextDescription": "Easily get your co-operative's social balance sheet for each period in which you have loaded your co-operative shares.",
    "errorTryLater": "There has been an error. Please try again later, if it persists contact the site adminsitrator.",
    "errorInPostedData": "There has been an error with data. Please, check your data."
  },
  es : {
    "signIn": "Inicie sesión",
    "header-title-1": "COOBS:",
    "header-title-2": "Balance Social Cooperativo",
    "header-subtitle": "Una herramienta que le facilitará realizar el seguimiento de las acciones de su organización social, guiadas por los principios cooperativos y los objetivos de desarrollo sustentable.",
    "section-metrics-title": "Métricas y seguimiento",
    "section-metrics-subtitle": "La herramienta la brindará la posibilidad de realizar un seguimiento de su actividad social en tiempo real, puediendo medir la incidencia de sus acciones.",
    "section-bs-title": "Balance social orgánico",
    "section-bs-subtitle": "Coobs brinda la posibilidad de planificar acciones futuras para guiar el desempeño social de su organización mediante objetivos basados en los valores cooperativos.",
    "signup": "Registrarse",
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
    "repeatPassword": "Repita la contraseña",
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
    "section-labs-text": "Desarrollado en FiqusLabs, un espacio donde creamos tecnología de código abierto orientada a la comunidad.",
    "firstImageTextTitle": "Cargue las acciones que su cooperativa realiza",
    "firstImageTextDescription": "En COOBS puede cargar las acciones que su cooperativa realiza relacionadas con cada principio cooperativo.",
    "secondImageTextTitle": "Vea toda su actividad cooperativa",
    "secondImageTextDescription": "Podrás ver diariamente lo que haces en tu cooperativa en relación con cada principio cooperativo permitiéndote tomar acciones para mejorarlo.",
    "thirdImageTextTitle": "Obtenga su balance anual",
    "thirdImageTextDescription": "Obtenga fácilmente el balance social de su cooperativa para cada período en el que haya cargado las acciones de su cooperativa.",
    "errorTryLater": "Se produjo un error. Por favor intente más tarde, si el problema persiste contacto al administrador del sitio.",
    "errorInPostedData": "Se produjo un error con los datos. Por favor, verifica los datos ingresados."
  }
}
$.tr.dictionary(langDict);

function setLang(langKey, langDesc) {
  $.tr.language(langKey);

  var tr = $.tr.translator();
  Object.keys(langDict[langKey]).forEach((key) => {
    $('#' + key).text(tr(key));
  });

  $('#language').html(langDesc);
  $("#coopBusinessName").attr('placeholder', tr("coopBusinessName"));
  $("#firstName").attr('placeholder', tr("firstName"));
  $("#lastName").attr('placeholder', tr("lastName"));
  $("#email").attr('placeholder', tr("email"));
  $("#password").attr('placeholder', tr("password"));
  $("#repeatPassword").attr('placeholder', tr("repeatPassword"));


}

$(document).ready(function() {

  // 'es' => default
  setLang('es', 'Español');

  $('.lang-option').click(function() {
    setLang($(this).data('value'), $(this).html());
  });
});