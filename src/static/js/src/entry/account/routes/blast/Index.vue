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

    <contact-us :ga-label="ga.userPortal.labels.blast" is-blast>
      <template #text>
        To update your subscription to The Blast, contact us at
      </template>
    </contact-us>
  </div>
</template>

<script>
import userMixin from '../../store/user/mixin';
import routeMixin from '../mixin';

import Current from './containers/CurrentContainer.vue';
import Former from './containers/FormerContainer.vue';

import ContactUs from '../../components/ContactUs.vue';

export default {
  name: 'BlastRoute',

  components: { ContactUs, Current, Former },

  mixins: [routeMixin, userMixin],
};
</script>
