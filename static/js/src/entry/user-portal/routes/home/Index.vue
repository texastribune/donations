<template>
  <div>
    <p>This is home.</p>
    <ul>
      <li>
        <router-link :to="{ name: 'membership' }">Membership</router-link>
      </li>
      <li><router-link :to="{ name: 'payments' }">Payments</router-link></li>
      <li><router-link :to="{ name: 'blast' }">Blast</router-link></li>
      <li>
        <router-link :to="{ name: 'blast-payments' }"
          >Blast Payments</router-link
        >
      </li>
    </ul>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'Index',
};
</script>
