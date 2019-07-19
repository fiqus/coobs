<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-4 offset-sm-4">
        <form v-on:submit.prevent="submit" class="needs-validation" novalidate>
          <div class="form-group">
            <label>Email: </label>
            <input type="email" v-model="user.email" class="form-control" />
            <div class="invalid-feedback"></div>
          </div>
          <div class="form-group">
            <label>Password: </label>
            <input type="password" v-model="user.password" class="form-control" />
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        email: "",
        pass: ""
      }
    }
  },
  methods: {
    submit(aa) {
      console.log(`Email: ${this.user.email}`);
      console.log(`Password: ${this.user.password}`);
    }
  }
}
</script>

