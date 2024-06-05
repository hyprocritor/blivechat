<template>
  <yt-live-chat-author-chip>
    <span id="author-name" dir="auto" class="style-scope yt-live-chat-author-chip"
          :class="{ member: isInMemberMessage }"
          :type="authorTypeText"
    >
      <template>{{ authorName }}</template>
       <img v-if="accompany>0" :src="`/static/img/accompany/${accompanyBadge}`"
            class="style-scope yt-live-chat-author-badge-renderer" :alt="accompanyBadgeReadableText"
       >
      <!-- 这里是已验证勋章 -->
      <span id="chip-badges" class="style-scope yt-live-chat-author-chip"></span>
    </span>
    <span id="chat-badges" class="style-scope yt-live-chat-author-chip">
      <author-badge v-if="isInMemberMessage" class="style-scope yt-live-chat-author-chip"
                    :isAdmin="false" :privilegeType="privilegeType"
      ></author-badge>
      <template v-else>
        <author-badge v-if="authorType === AUTHOR_TYPE_ADMIN" class="style-scope yt-live-chat-author-chip"
                      isAdmin :privilegeType="0"
        ></author-badge>
        <author-badge v-if="privilegeType > 0" class="style-scope yt-live-chat-author-chip"
                      :isAdmin="false" :privilegeType="privilegeType"
        ></author-badge>
      </template>
    </span>
  </yt-live-chat-author-chip>
</template>

<script>
import AuthorBadge from './AuthorBadge'
import * as constants from './constants'
import { accompanyFileNames, accompanyRages } from "./constants"

export default {
  name: 'AuthorChip',
  components: {
    AuthorBadge
  },
  props: {
    isInMemberMessage: Boolean,
    authorName: String,
    authorType: Number,
    privilegeType: Number,
    accompany: Number,
  },
  data() {
    return {
      AUTHOR_TYPE_ADMIN: constants.AUTHOR_TYPE_ADMIN
    }
  },
  computed: {
    authorTypeText() {
      return constants.AUTHOR_TYPE_TO_TEXT[this.authorType]
    },
    accompanyBadgeReadableText() {
      return `${this.accompany.toString()}days`
    },
    accompanyBadge() {
      for (let range in accompanyRages) {
        const min = accompanyRages[range][0]
        const max = accompanyRages[range][1]
        if (min < this.accompany && this.accompany <= max) {
          console.log("user", this.accompany, min, max)
          return accompanyFileNames[range]
        }
      }
      return null
    }
  }
}
</script>

<style src="@/assets/css/youtube/yt-live-chat-author-chip.css"></style>
