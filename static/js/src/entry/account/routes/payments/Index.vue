<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      Your Donations
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg"><payments /></div>

    <appeal />

    <help payments />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Appeal from '../home/containers/AppealContainer.vue';
import Help from '../../components/Help.vue';
import Payments from './containers/PaymentsContainer.vue';

export default {
  name: 'PaymentsRoute',

  components: { Appeal, Payments, Help },

  mixins: [routeMixin],
};
</script>
