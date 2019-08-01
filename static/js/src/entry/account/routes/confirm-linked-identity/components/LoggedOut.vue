<template>
  <div>
    <h1 class="has-xl-btm-marg">Log in to confirm your linked email</h1>
    <p class="t-space-heading-m has-b-btm-marg">Copy copy copy copy copy</p>
    <button @click="$emit('logIn')">Log in</button>
  </div>
</template>

<script>
export default {
  name: 'ConfirmLinkedIdentityLoggedOut',
};
</script>
