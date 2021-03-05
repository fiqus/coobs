<template>
  <div class="help-inapp help-content-container" v-html="loadAndShowHelp()"></div>
</template>
<script>
export default {
  data() {
    return {
      lang: this.$store.state.lang || this.$i18n.locale(),
      loadAndShowHelp() {
        const axios = require("axios").create({headers: {}});
        axios.get("/help/"+this.lang+".html")
          .then((res) => $(".help-content-container").html(res.data));
      }
    }
  }
}
</script>
