<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-xl-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg"><blast-detail /></div>

    <help blast :display="{ hasTopPadding: true }" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Help from '../../components/Help.vue';
import BlastDetail from './containers/BlastDetailContainer.vue';

export default {
  name: 'BlastRoute',

  components: { Help, BlastDetail },

  mixins: [routeMixin],
};
</script>
