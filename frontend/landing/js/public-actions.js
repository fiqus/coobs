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

  function fetchActions() {
    const data = {more, limit};
    $.ajax({
      url: `${scheme}://${hostname}/api/public-actions`,
      type: "GET",
      headers: {},
      data,
      cache: false,
      success: onSucess,
      error: onError
    });
  }

  function onSucess(data) {
    console.error(data); // @TODO CONTINUE HERE!
  }
  function onError(err) {
    console.error(err); // @TODO Add better error handling here!
  }

  window.viewActionDetail = (el) => {
    console.error(el);
  };

  function setTimeout(delay) {
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
    if (bottomOfWindow && scrollOrWheel && !this.noMoreData && !this.loading) {
      setTimeout(5000);
      fetchActions();
    }
  }
  window.addEventListener("scroll", onScroll);
  window.addEventListener("wheel", onScroll);
  fetchActions(); // Initial fetch call
});
