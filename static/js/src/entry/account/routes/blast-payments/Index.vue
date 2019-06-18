<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg"><blast-payments /></div>

    <help blast-payments :display="{ hasTopPadding: true }" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Help from '../../components/Help.vue';
import BlastPayments from './containers/BlastPaymentsContainer.vue';

export default {
  name: 'BlastPaymentsRoute',

  components: { Help, BlastPayments },

  mixins: [routeMixin],
};
</script>
