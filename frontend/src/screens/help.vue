<template>
  <div class="help-inapp help-content-container" v-html="loadAndShowHelp()"></div>
</template>
<script>
export default {
  computed: {
    lang() {
      return this.$store.state.lang || this.$i18n.locale();
    }
  },
  methods: {
    loadAndShowHelp() {
      const axios = require("axios").create({headers: {}});
      axios.get("/help/"+this.lang+".html")
        // @TODO Avoid jQuery usage below to put help contents into the div
        .then((res) => $(".help-content-container").html(res.data));
    }
  }
}
</script>
