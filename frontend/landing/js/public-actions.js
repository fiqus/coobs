$(() => {
  const { scheme, hostname } =
    process.env.NODE_ENV === "production"
      ? { scheme: "https"
        , hostname: window.location.hostname }
      : { scheme: "http"
        , hostname: "localhost:8000" };

  const limit = 2; // @TODO Change it to 10!
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
    console.error(action);
    const tpl = $("#public-actions-table tr.action-tpl").clone().removeClass(["action-tpl", "hidden"]);//.eq(0);
    $(".public-action-date", tpl).html(action.date); // @TODO Parse date
    $(".public-action-coop", tpl).html(action.cooperativeName);
    $(".public-action-name", tpl).html(action.name);
    $(".public-action-desc", tpl).html(action.description); // @TODO Parse markdown/html
    $(".public-action-principles", tpl).html("-"); // @TODO Parse principles
    $(".public-action-actions button", tpl).data("id", action.id);
    $("#public-actions-table tbody").append(tpl);
    console.error(tpl);
  }

  window.viewActionDetail = (el) => {
    // @TODO Complete this!
    const id = $(el).data("id");
    console.error("SHOW DETAILS FOR ACTION: "+id);
  };

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
    const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
    if (bottomOfWindow && scrollOrWheel && !noMoreData && !loading) {
      fetchActions();
    }
  }
  window.addEventListener("scroll", onScroll);
  window.addEventListener("wheel", onScroll);
  fetchActions(); // Initial fetch call
});
