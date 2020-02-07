<template>
  <div>
    <h1
      class="has-ump-top-padding has-ump-side-padding has-l-btm-marg t-size-xl"
    >
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box c-detail-box--from-l">
        <div class="has-xxxl-btm-marg"><detail /></div>

        <internal-nav />
      </section>
    </div>

    <help blast-payments />
  </div>
</template>

<script>
import Help from '../../components/Help.vue';
import userMixin from '../../store/user/mixin';
import routeMixin from '../mixin';
import Detail from './components/Detail.vue';
import InternalNav from './components/InternalNav.vue';

export default {
  name: 'BlastPaymentsRoute',

  components: { Help, Detail, InternalNav },

  mixins: [routeMixin, userMixin],
};
</script>
