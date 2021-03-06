import './vendor/jquery/jquery.min.js';
import './vendor/bootstrap/js/bootstrap.bundle.min.js';
import './vendor/jquery-easing/jquery.easing.min.js';
import './vendor/translate/jquery.tr.js';
import './vendor/translate/translations.js';
import "magnific-popup/dist/jquery.magnific-popup.min.js"
import './js/jqBootstrapValidation.js';
import './js/contact_me.js';
import './js/public-actions.js';

import * as utils from '../src/utils.js';
$.utils = utils;

import {loadLocalMessage} from "../src/i18n";
$.tr.langdata = {en: loadLocalMessage("en"), es: loadLocalMessage("es")};

import './vendor/fontawesome-free/css/all.min.css';
import "magnific-popup/dist/magnific-popup.css"
import './css/landing.css';
import './css/custom.css';
import "../assets/css/help.css"

import 'bootstrap/dist/css/bootstrap.min.css';
