<template>
  <div>
    <router-view />
    <router-link :to="'?amount=23&installmentPeriod=yearly'">Foo</router-link>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>
