import './assets/main.css'

import { createApp, createBlock, createElementBlock } from 'vue'
import Calc from './Calculator.vue'
import HeadlinesVue from './components/Headlines.vue'

createApp(Calc).mount('#calc')
createApp(HeadlinesVue).mount('#headline')

