<template>
  <div class="table-responsive infinite-scroll">
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
      <tfoot>
        <tr>
          <td :colspan="headers.length + (actions.hideViewDetailButton?0:1)">
            <div v-if="noMoreData && noMoreDataMsg" class="bold">{{noMoreDataMsg}}</div>
            <div v-else>{{$t("scrollMoreData")}}</div>
          </td>
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
      loading: false,
      noMoreData: false
    };
  },
  mounted() {
    window.addEventListener("scroll", this.onScroll);
    window.addEventListener("wheel", this.onScroll);
    this.$emit("onGetMore", {more: this.count, done: this.onAddMore});
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll);
    window.removeEventListener("wheel", this.onScroll);
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
      this.removeTimeout();
      if (elements && elements.length) {
        this.elements.push(...elements);
        this.count++;
      } else {
        this.noMoreData = true;
      }
    },
    onScroll(ev) {
      const scrollOrWheel = ev.deltaY === undefined || ev.deltaY > 0;
      const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if (bottomOfWindow && scrollOrWheel && !this.noMoreData && !this.loading) {
        this.setTimeout(5000);
        this.$emit("onGetMore", {more: this.count, done: this.onAddMore});
      }
    },
    onViewDetail(elem) {
      this.$emit("onViewDetail", elem);
    },
    setTimeout(delay) {
      this.loading = setTimeout(() => this.removeTimeout(), delay);
    },
    removeTimeout() {
      if (this.loading) {
        clearTimeout(this.loading);
      }
      this.loading = false;
    }
  }
};
</script>
