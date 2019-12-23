<template>
  <div class="form-group">

    <label v-if="label">
      {{label}}
    </label>
    <Multiselect class="custom-select"
      v-model="value" 
      tag-placeholder="Select partners" 
      placeholder="Select partners" 
      label="partner" 
      track-by="id" 
      :options="options" 
      :multiple="true" 
      :taggable="true" 
      @tag="addTag">
    </Multiselect>

    <select class="custom-select" :class="{'is-invalid': error}" v-model="value" @input="onInput">
      <option selected value="">{{defaultValue}}</option>
      <option v-for="option in options" :key="option.id" :value="option.id">
        {{option.name}}
      </option>
    </select>
    <div v-if="error" class="invalid-feedback">
      {{errorMessage}}
    </div>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  export default {
    components: {
      Multiselect
    },
    data () {
      return {
        value: [
          { name: 'Javascript', code: 'js' }
        ],
        options: [
          { name: 'Vue.js', code: 'vu' },
          { name: 'Javascript', code: 'js' },
          { name: 'Open Source', code: 'os' }
        ]
      }
    },
    methods: {
      addTag (newTag) {
        const tag = {
          name: newTag,
          code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(tag)
        this.value.push(tag)
      }
    }
  }
  }
</script>