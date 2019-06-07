<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-xl-btm-marg has-ump-side-padding t-size-xl">
      Your Membership
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg"><membership /></div>

    <appeal />

    <help membership />
  </div>
</template>

<script>
import Membership from './containers/MembershipContainer.vue';
import routeMixin from '../../mixins/route';
import Appeal from '../../components/Appeal.vue';
import Help from '../../components/Help.vue';

export default {
  name: 'Index',

  components: { Appeal, Help, Membership },

  mixins: [routeMixin],
};
</script>
