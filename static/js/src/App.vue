<template>
  <div>
    <router-view />
    <router-link :to="'?amount=58'">Test</router-link>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>
