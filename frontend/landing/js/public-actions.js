$(() => {
  const { scheme, hostname } =
    process.env.NODE_ENV === "production"
      ? { scheme: "https"
        , hostname: window.location.hostname }
      : { scheme: "http"
        , hostname: "localhost:8000" };

  const limit = 10;
  let more = 0;
  let loading = false;
  let noMoreData = false;

  function fetchActions() {
    setupTimeout(5000);
    const data = {more, limit};
    $.ajax({
      url: `${scheme}://${hostname}/api/public-actions/`,
      type: "GET",
      headers: {},
      data,
      cache: false,
      success: onSuccess,
      error: onError
    });
  }

  function onSuccess(data) {
    removeTimeout();
    if (data && data.actions && data.actions.length) {
      data.actions.map(appendAction);
      more++;
    } else {
      noMoreData = true;
      $("#public-actions-scroll-more").addClass("hidden");
      $("#public-actions-no-more").removeClass("hidden");
    }
  }
  function onError(err) {
    console.error(err); // @TODO Add better error handling here!
  }

  function appendAction(action) {
    const tpl = $("#public-actions-table tr.action-tpl").clone().removeClass(["action-tpl", "hidden"]);
    $(".public-action-date", tpl).html(action.date); // @TODO Format date (but need to support on language change)
    $(".public-action-coop", tpl).html($.utils.capitalizeFirstChar(action.cooperativeName));
    $(".public-action-name", tpl).html(action.name);
    $(".public-action-principles", tpl).html(parsePrinciples(action.principles));
    $(".public-action-actions button", tpl).data("id", action.id);
    $("#public-actions-table tbody").append(tpl);
  }

  function parsePrinciples(principles) {
    const translator = $.tr.translator();
    let result = "";
    principles.forEach((principle) => {
      const princripleName = translator(principle.nameKey);
      result = result.concat(`<div><span class="multiselect__tag langkey-${principle.nameKey}">${princripleName}</span></div>`)
    });
    return result;
  }

  function parseSustainableDevelopmentGoals(goals) {
    const translator = $.tr.translator();
    let result = "";
    goals.forEach((goal) => {
      const goalName = translator(goal.nameKey, goal.name);
      result = result.concat(`<div><span class="multiselect__tag langkey-${goal.nameKey}">${goalName}</span></div>`)
    });
    return result;
  }

  function formatNumber(number) {
    return $.utils.parseNumber(number, $.tr.language());
  }

  function formatDate(date) {
    return $.utils.formatToUIDate(date, $.tr.language());
  }

  window.viewActionDetail = (el) => {
    const id = $(el).data("id");
    $.ajax({
      url: `${scheme}://${hostname}/api/public-actions/${id}`,
      type: "GET",
      headers: {},
      data: {},
      cache: true,
      success: (data) => data && data.action ? openActionModal(data.action) : null,
      error: onError
    });
  };

  function openActionModal(action) {
    const body = $("#detailModal .modal-body");

    $("[name=cooperativeName]", body).html(action.cooperativeName);
    $("[name=name]", body).html(action.name);
    $("[name=description]", body).html($.utils.sanitizeMarkdown(action.description||""));
    $("[name=startingDate]", body).html(formatDate(action.date));
    $("[name=investedHours]", body).html(formatNumber(action.investedHours));
    $("[name=investedMoney]", body).html("$"+formatNumber(action.investedMoney));
    $("[name=principles]", body).html(parsePrinciples(action.principles));
    if ((action.sustainableDevelopmentGoals||[]).length === 0) {
      $(".sustainableDevelopmentGoals", body).hide();
    } else {
      $(".sustainableDevelopmentGoals", body).show();
      $("[name=sustainableDevelopmentGoals]", body).html(parseSustainableDevelopmentGoals(action.sustainableDevelopmentGoals));
    }

    $.magnificPopup.open({
      items: {
        src: ".modal-dialog",
        type: "inline"
      }
    });
  }

  function setupTimeout(delay) {
    loading = setTimeout(removeTimeout, delay);
  }
  function removeTimeout() {
    if (loading) {
      clearTimeout(loading);
    }
    loading = false;
  }

  function onScroll(ev) {
    const scrollOrWheel = ev.deltaY === undefined || ev.deltaY > 0;
    const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight > document.documentElement.offsetHeight - 5;
    if (bottomOfWindow && scrollOrWheel && !noMoreData && !loading) {
      fetchActions();
    }
  }

  if ($("section.public-actions")[0]) {
    window.addEventListener("scroll", onScroll);
    window.addEventListener("wheel", onScroll);
    fetchActions(); // Initial fetch call
  }
});
