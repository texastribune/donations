<template>
  <div>
    <h2 class="has-xl-btm-marg">Why do you support The Texas Tribune?</h2>
    <ul class="c-ambassador-socials has-xl-btm-marg">
      <li><a href="#">Twitter</a></li>
      <li><a href="#">Facebook</a></li>
      <li><a href="#">Email</a></li>
    </ul>
    <referral-form />
  </div>
</template>

<script>
import ReferralForm from '../containers/ReferralFormContainer.vue';

export default {
  name: 'ReferralLinks',

  components: { ReferralForm },
};
</script>
