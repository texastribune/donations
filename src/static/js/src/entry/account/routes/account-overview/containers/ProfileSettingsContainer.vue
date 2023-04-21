<template>
  <profile-settings
    :first-name="user.firstName"
    :last-name="user.lastName"
    :email="user.email"
    :zip="user.zip"
  />
</template>

<script>
import userMixin from '../../../store/user/mixin';

import ProfileSettings from '../components/ProfileSettings.vue';

export default {
  name: 'SummmaryProfileSettingsContainer',

  components: { ProfileSettings },

  mixins: [userMixin],
};
</script>
