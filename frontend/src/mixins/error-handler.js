export default {
  methods: {
    handleError(err) {
      if (err.response.data.detail) {
        this.error.message = err.response.data.detail;
      } else if (Object.keys(err.response.data).length) {
        this.error.message = Object.values(err.response.data).flat().join('<br>');
      } else {
        this.error.message = "backendServicesError";
      }
      this.error.exists = true;
    }
  },
  data() {
    return {
      error: {
        exists: false,
        message: "",
        backgroundClass: "bg-danger"
      }
    }
  }
};
