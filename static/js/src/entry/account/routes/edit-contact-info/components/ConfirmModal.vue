<template>
  <modal name="modal" width="80%" height="auto" :max-width="450" adaptive>
    <div class="c-modal">
      <div class="c-modal__top l-align-center-children">
        <h2 class="t-size-m t-align-center">You have unsaved changes</h2>
      </div>
      <ul class="c-modal__buttons l-width-full">
        <li>
          <base-button
            text="Abandon changes"
            :display="{ size: 's' }"
            @onClick="$emit('onLeave')"
          />
        </li>
        <li>
          <base-button
            text="Return to form"
            :display="{ size: 's' }"
            @onClick="$emit('onReturn')"
          />
        </li>
      </ul>
    </div>
    <button
      class="c-modal__close has-bg-white has-text-gray"
      aria-label="close modal"
      @click="$emit('onReturn')"
    >
      <icon name="close" :display="{ size: 'xxs', color: 'gray' }" />
    </button>
  </modal>
</template>

<script>
export default {
  name: 'EditContactInfoModal',
};
</script>
