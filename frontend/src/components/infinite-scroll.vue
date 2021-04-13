<template>
  <div class="table-responsive">
    <table class="table table-striped">
      <thead>
        <tr>
          <th class="text-truncate" v-for="header in headers" :key="header.key">
            {{ $t(header.value, header.value) }}
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="elem in elements" :key="elem.id">
          <td class="text-truncate-wrap cursor-pointer" v-for="header in headers" :key="header.key" v-html="parseElem(header, elem)"></td>
          <td v-if="!actions.hideViewDetailButton" class="actions">
            <button class="btn btn-success" @click.stop="onViewDetail(elem)" :title="$t('quickView')"><i class="fa fa-eye"></i></button>
          </td>
        </tr>
      </tbody>
      <tfoot v-if="noMoreData && noMoreDataMsg">
        <tr>
          <td :colspan="headers.length + (actions.hideViewDetailButton?0:1)">{{noMoreDataMsg}}</td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>
<script>
export default {
  props: {
    headers: {
      type: Array,
      default: [],
      required: true
    },
    elements: {
      type: Array,
      default: [],
      required: true
    },
    actions: {
      type: Object,
      default: {
        hideViewDetailButton: false
      }
    },
    noMoreDataMsg: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      count: 0,
      noMoreData: false
    };
  },
  mounted() {
    window.addEventListener("scroll", this.onScroll);
    this.$emit("onGetMore", {more: this.count, done: this.onAddMore});
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll);
  },
  methods: {
    parseElem(header, elem) {
      if (header.parser) {
        try {
          return header.parser(elem) || "";
        } catch (err) {
          console.trace(`Can't parse the element for '${header.key}'!`, err);
        }
      }
      return elem[header.key] || "";
    },
    onAddMore(elements) {
      this.elements.push(...elements);
      this.count++;
    },
    onScroll() {
      const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if (bottomOfWindow) {
        this.$emit("onGetMore", {more: this.count, done: this.onAddMore});
      }
    },
    onViewDetail(elem) {
      this.$emit("onViewDetail", elem);
    }
  }
};
</script>
