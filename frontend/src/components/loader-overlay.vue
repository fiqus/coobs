<template>
    <div :class="[loading?'overlay':'']">
      <h1 class="loading-text" v-bind:style="loading? '': 'display:none;'">{{$t('loading')}}</h1>
      <!-- <slot/> -->
      <div class="lds-roller" v-bind:style="loading?'left:40%;':'display:none;'">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>      
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

  .lds-roller {
    position: fixed;
    top: 48%; 
    left: 40%;
    display: inline-block;
    width: 80px;
    height: 80px;
    z-index: 2;
  }
  .lds-roller div {
    animation: lds-roller 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    transform-origin: 40px 40px;
  }
  .lds-roller div:after {
    content: " ";
    display: block;
    position: absolute;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    /* background: rgb(53, 182, 201); */
    background: white;
    margin: -4px 0 0 -4px;
  }
  .lds-roller div:nth-child(1) {
    animation-delay: -0.036s;
  }
  .lds-roller div:nth-child(1):after {
    top: 63px;
    left: 63px;
  }
  .lds-roller div:nth-child(2) {
    animation-delay: -0.072s;
  }
  .lds-roller div:nth-child(2):after {
    top: 68px;
    left: 56px;
  }
  .lds-roller div:nth-child(3) {
    animation-delay: -0.108s;
  }
  .lds-roller div:nth-child(3):after {
    top: 71px;
    left: 48px;
  }
  .lds-roller div:nth-child(4) {
    animation-delay: -0.144s;
  }
  .lds-roller div:nth-child(4):after {
    top: 72px;
    left: 40px;
  }
  .lds-roller div:nth-child(5) {
    animation-delay: -0.18s;
  }
  .lds-roller div:nth-child(5):after {
    top: 71px;
    left: 32px;
  }
  .lds-roller div:nth-child(6) {
    animation-delay: -0.216s;
  }
  .lds-roller div:nth-child(6):after {
    top: 68px;
    left: 24px;
  }
  .lds-roller div:nth-child(7) {
    animation-delay: -0.252s;
  }
  .lds-roller div:nth-child(7):after {
    top: 63px;
    left: 17px;
  }
  .lds-roller div:nth-child(8) {
    animation-delay: -0.288s;
  }
  .lds-roller div:nth-child(8):after {
    top: 56px;
    left: 12px;
  }
  @keyframes lds-roller {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }  
</style>