<script lang="ts">
  import Calc from './bod/Calculator.vue';
  import Weather from './bod/Weather.vue';

  export default {
    components: {
      Calc,
      Weather
    }
  }
</script>

<template>
  <div class="container">
    <calc class="comp1"></calc>
    <weather class="comp2"></weather>
  </div>

</template>

<style scoped>
  .container {
    margin-top: 50px;
    display: flex;
    justify-content: space-evenly;
  }

  .component {
    position: relative;
  }

  .comp1 {
    background: linear-gradient(100deg, rgba(55, 55, 55, 0.016), #ac9011);
  }

  .comp2 {
    background: linear-gradient(100deg, #ac9011, rgba(55, 55, 55, 0.016));
  }
</style>