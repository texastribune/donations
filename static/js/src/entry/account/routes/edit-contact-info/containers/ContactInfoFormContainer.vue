<template>
  <button @click="fooBar">Update identity</button>
</template>

<script>
import userMixin from '../../../store/user/mixin';

export default {
  name: 'AccountFormContainer',

  mixins: [userMixin],

  methods: {
    fooBar() {
      this.updateUser({
        postal_code: 12349,
      });
    },
  },
};
</script>
