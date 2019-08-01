<template>
  <modal name="modal" width="80%" :height="200" :max-width="450" adaptive>
    <div class="c-modal has-xl-padding">
      <h2 class="t-size-m t-align-center has-b-btm-marg">
        You have unsaved changes
      </h2>
      <button @click="$emit('onLeave')">Abandon changes</button>
      <button @click="$emit('onReturn')">Return to form</button>
    </div>
  </modal>
</template>

<script>
export default {
  name: 'EditContactInfoModal',
};
</script>
