<template>
    <div :class="[loading?'overlay':'']">
      <!-- FIXME we should decide wheter to use loading text or not -->
      <h1 class="loading-text" v-bind:style="loading? '': 'display:none;'">{{$t('loading')}}</h1>
      <!-- <slot/> -->
    </div>
</template>

<script>
  export default {
    props: {
      loading: {
          type: Boolean
        }
    }
  }
</script>

// FIXME we should remove loading-text styles if we decide not to use loading text
<style scoped>
  .overlay{
    width: 100%; 
    height:100%; 
    position:absolute; 
    top:0;
    left: 0;
    z-index: 1;
    background-color: rgba(0,0,0,0.5);
  }
  .loading-text{
    color:white; 
    position: fixed;
    top: 50%; 
    left: 46%;
    z-index: 2;
  }

  /* .loading-text:after {
    content: ' .';
    animation: dots 1s steps(5, end) infinite;
  }

  @keyframes dots {
    0%, 20% {
      color: rgb(53, 182, 201);
      text-shadow:
        .25em 0 0 rgb(53, 182, 201),
        .5em 0 0 rgb(53, 182, 201);}
    40% {
      color: white;
      text-shadow:
        .25em 0 0 rgb(53, 182, 201),
        .5em 0 0 rgb(53, 182, 201);}
    60% {
      text-shadow:
        .25em 0 0 white,
        .5em 0 0 rgb(53, 182, 201);}
    80%, 100% {
      text-shadow:
        .25em 0 0 white,
        .5em 0 0 white}
  }   */
</style>