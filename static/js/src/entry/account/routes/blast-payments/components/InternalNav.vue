<template>
  <user-internal-nav show-blast-subscription show-renew-blast>
    <template v-slot:blast-text>
      More about your subscription
    </template>
  </user-internal-nav>
</template>

<script>
export default {
  name: 'BlastPaymentsInternalNav',
};
</script>
