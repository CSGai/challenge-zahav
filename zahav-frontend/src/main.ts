import './assets/main.css'
import { createApp } from 'vue'

import root from './components/RootComp.vue'
import Headlines from './components/Headlines.vue'


// createApp(root).mount('#root');

const rootDOM = createApp(root);

rootDOM.mount('#root')

createApp(Headlines).mount('#headline');