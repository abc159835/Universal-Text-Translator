import { createApp } from "vue";
import App from "./App.vue";
import mitt from "mitt";

// import "~/styles/element/index.scss";

//import ElementPlus from "element-plus";
// import all element css, uncommented next line
import "element-plus/dist/index.css";

// or use cdn, uncomment cdn link in `index.html`

import "~/styles/index.scss";
import "uno.css";

// If you want to use ElMessage, import it.
import "element-plus/theme-chalk/src/message.scss";

const bus = mitt()
const app = createApp(App);

import router from './router'
app.use(router)
//app.use(ElementPlus);
app.config.globalProperties.$bus = bus

app.mount("#app");


