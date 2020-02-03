<template>
  <profile-settings
    :first-name="user.firstName"
    :last-name="user.lastName"
    :email="user.email"
    :zip="user.zip"
  />
</template>

<script>
import ProfileSettings from '../components/ProfileSettings.vue';
import userMixin from '../../../store/user/mixin';

export default {
  name: 'SummmaryProfileSettingsContainer',

  components: { ProfileSettings },

  mixins: [userMixin],
};
</script>
