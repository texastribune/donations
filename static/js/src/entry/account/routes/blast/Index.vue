<template>
  <div>
    <h1
      class="has-ump-top-padding has-xl-btm-marg has-ump-side-padding t-size-xl"
    >
      The Blast Newsletter
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg">
      <current /> <former />
    </div>

    <help blast />
  </div>
</template>

<script>
import Help from '../../components/Help.vue';
import userMixin from '../../store/user/mixin';
import routeMixin from '../mixin';
import Current from './containers/CurrentContainer.vue';
import Former from './containers/FormerContainer.vue';

export default {
  name: 'BlastRoute',

  components: { Help, Current, Former },

  mixins: [routeMixin, userMixin],
};
</script>
