<template>
  <nav>
    <ul>
      <li>
        <router-link :to="{ name: 'home' }">Account Overview</router-link>
      </li>
      <li>
        <router-link :to="{ name: 'membership' }">Membership</router-link>
      </li>
      <li>
        <router-link :to="{ name: 'payments' }">Donation History</router-link>
      </li>
      <li>
        <router-link :to="{ name: 'blast' }">The Blast Newsletter</router-link>
      </li>
      <li>
        <router-link :to="{ name: 'blast-payments' }"
          >Payment History</router-link
        >
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'SideNav',
};
</script>
