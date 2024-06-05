<template>
  <yt-live-chat-paid-message-renderer class="style-scope yt-live-chat-item-list-renderer" allow-animations
                                      :show-only-header="!content" :style="{
      '--yt-live-chat-paid-message-primary-color': color.contentBg,
      '--yt-live-chat-paid-message-secondary-color': color.headerBg,
      '--yt-live-chat-paid-message-header-color': color.header,
      '--yt-live-chat-paid-message-author-name-color': color.authorName,
      '--yt-live-chat-paid-message-timestamp-color': color.time,
      '--yt-live-chat-paid-message-color': color.content
    }"
                                      :blc-price-level="priceConfig.priceLevel"
  >
    <div id="card" class="style-scope yt-live-chat-paid-message-renderer">
      <div id="header" class="style-scope yt-live-chat-paid-message-renderer">
        <img-shadow id="author-photo" height="40" width="40" class="style-scope yt-live-chat-paid-message-renderer"
                    :imgUrl="avatarUrl"
        ></img-shadow>
        <div id="header-content" class="style-scope yt-live-chat-paid-message-renderer">
          <div id="header-content-primary-column" class="style-scope yt-live-chat-paid-message-renderer">
            <div>
              <div id="author-name" class="style-scope yt-live-chat-paid-message-renderer">{{ authorName }}</div>
              <img v-if="accompany>0" :src="`/static/img/accompany/${accompanyBadge}`"
                   class="style-scope yt-live-chat-author-badge-renderer" :alt="accompanyBadgeReadableText"
              >
            </div>
            <div id="purchase-amount" class="style-scope yt-live-chat-paid-message-renderer">{{ showPriceText }}</div>
          </div>
          <span id="timestamp" class="style-scope yt-live-chat-paid-message-renderer">{{ timeText }}</span>
        </div>
      </div>
      <div id="content" class="style-scope yt-live-chat-paid-message-renderer">
        <div id="message" dir="auto" class="style-scope yt-live-chat-paid-message-renderer">{{ content }}</div>
      </div>
    </div>
  </yt-live-chat-paid-message-renderer>
</template>

<script>
import ImgShadow from './ImgShadow'
import * as constants from './constants'
import * as utils from '@/utils'
import { accompanyFileNames, accompanyRages } from "./constants"

export default {
  name: 'PaidMessage',
  components: {
    ImgShadow
  },
  props: {
    avatarUrl: String,
    authorName: String,
    price: Number, // 价格，人民币
    priceText: String,
    time: Date,
    content: String,
    accompany: Number,
  },
  computed: {
    priceConfig() {
      return constants.getPriceConfig(this.price)
    },
    color() {
      return this.priceConfig.colors
    },
    showPriceText() {
      return this.priceText || `CN¥${utils.formatCurrency(this.price)}`
    },
    timeText() {
      return utils.getTimeTextHourMin(this.time)
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

<style src="@/assets/css/youtube/yt-live-chat-paid-message-renderer.css"></style>
