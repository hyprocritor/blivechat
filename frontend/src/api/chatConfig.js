import _ from 'lodash'

import { mergeConfig } from '@/utils'
export const defaultGuardSetting = [
  {
    start: 0,
    end: 30,
    url: '/static/img/accompany/NewBie.png'
  },
  {
    start: 30,
    end: 60,
    url: '/static/img/accompany/1month.png'
  },
  {
    start: 60,
    end: 180,
    url: '/static/img/accompany/2month.png'
  },
  {
    start: 180,
    end: 365,
    url: '/static/img/accompany/6month.png'
  },
  {
    start: 365,
    end: 732,
    url: '/static/img/accompany/12month.png'
  },
  {
    start: 732,
    end: 1097,
    url: '/static/img/accompany/24month.png'
  },
  {
    start: 1097,
    end: Number.MAX_VALUE,
    url: '/static/img/accompany/36month.png'
  }
]

export const DEFAULT_CONFIG = {
  minGiftPrice: 0.1,
  showDanmaku: true,
  showGift: true,
  showGiftName: false,
  mergeSimilarDanmaku: false,
  mergeGift: true,
  maxNumber: 60,

  blockGiftDanmaku: true,
  blockLevel: 0,
  blockNewbie: false,
  blockNotMobileVerified: false,
  blockKeywords: '',
  blockUsers: '',
  blockMedalLevel: 0,

  showDebugMessages: false,
  relayMessagesByServer: false,
  autoTranslate: false,
  giftUsernamePronunciation: '',
  importPresetCss: false,
  guardSetting: defaultGuardSetting, // [{ start: '', end: '', url: '' }, ...]
  emoticons: [], // [{ keyword: '', url: '' }, ...]

}


export function deepCloneDefaultConfig() {
  return _.cloneDeep(DEFAULT_CONFIG)
}

export function setLocalConfig(config) {
  config = mergeConfig(config, DEFAULT_CONFIG)
  window.localStorage.config = JSON.stringify(config)
}

export function getLocalConfig() {
  try {
    let config = JSON.parse(window.localStorage.config)
    config = mergeConfig(config, deepCloneDefaultConfig())
    sanitizeConfig(config)
    return config
  } catch {
    let config = deepCloneDefaultConfig()
    // 新用户默认开启调试消息，免得总有人问
    config.showDebugMessages = true
    return config
  }
}

export function sanitizeConfig(config) {
  let newEmoticons = []
  if (config.emoticons instanceof Array) {
    for (let emoticon of config.emoticons) {
      try {
        let newEmoticon = {
          keyword: emoticon.keyword,
          url: emoticon.url
        }
        if ((typeof newEmoticon.keyword !== 'string') || (typeof newEmoticon.url !== 'string')) {
          continue
        }
        newEmoticons.push(newEmoticon)
      } catch {
        continue
      }
    }
  }
  console.log("testa")
  // deal with the guardsetting parts   like emoticons
  let newGuardSettings = []
  if (config.guardSetting instanceof Array) {
    for (let guardSetting of config.guardSetting) {
      try {
        let newGuardSetting = {
          start: guardSetting.keyword,
          end: guardSetting.end,
          url: guardSetting.url
        }
        console.log("test")
        if ((typeof newGuardSetting.start !== 'number') || (typeof newGuardSetting.end !== 'number')
          || (typeof newGuardSetting.url !== 'string')) {
          continue
        }
        newGuardSettings.push(newGuardSetting)
      } catch {
        continue
      }
    }
  }
}
