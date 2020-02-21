<template>
  <div v-if="pagination && dataLength" class="row">
    <div class="col-sm-12 col-md-5">
      <div class="" role="status" aria-live="polite">
        {{paginationMessage}}
      </div>
    </div>
    <div class="col-sm-12 col-md-7">
      <div class=" paging_simple_numbers">
        <ul class="justify-content-end pagination">
          <li class="paginate_button page-item previous" :class="{'disabled': !pagination.previous}">
            <button class="page-link" @click="goPrevious()">{{$t('previous')}}</button>
          </li>
          <li v-for="pageNumber in pagination.numPages" :key="pageNumber" class="paginate_button page-item " :class="{'active': pageNumber === pagination.page}">
            <button class="page-link" @click="goToPage(pageNumber)">{{pageNumber}}</button>
          </li>
          <li class="paginate_button page-item next" :class="{'disabled': !pagination.next}">
            <button class="page-link" @click="goNext()">{{$t('next')}}</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    dataLength: {
      type: Number,
      default: 0,
      required: true
    },
    pagination: {
      type: Object,
      default: null
    }
  },
  computed: {
    paginationMessage() {
      if (!this.pagination) {
        return;
      }
      const start = (this.pagination.pageSize * (this.pagination.page-1)) + 1;
      const end = this.dataLength < this.pagination.pageSize ? ((this.pagination.pageSize * (this.pagination.page-1)) + this.dataLength) : this.pagination.pageSize * this.pagination.page;
      return this.$t('paginationMessage', {start, end, count: this.pagination.count});
    }
  },
  methods: {
    goToPage(page) {
      this.$emit("goToPage", page);
    },
    goNext() {
      this.$emit("goNext");
    },
    goPrevious() {
      this.$emit("goPrevious");
    }
  }
};
</script>