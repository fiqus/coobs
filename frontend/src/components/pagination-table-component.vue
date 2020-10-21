<template>
  <div v-if="pagination && dataLength" class="d-sm-flex justify-content-sm-between align-items-sm-center">
    <div class="" role="status" aria-live="polite">
      {{paginationMessage}}
    </div>
    <div class=" paging_simple_numbers mt-3 mt-sm-0">
      <ul class="justify-content-start justify-content-sm-end pagination my-sm-auto">
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