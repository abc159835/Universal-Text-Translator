<template>
  <r-app-menu>
    <Menu :info="info" @project_change="project_change"></Menu>
  </r-app-menu>

  <l-navigation-drawer :style="slider_style">
    <TreeView :data="file_data" @content_change="content_change"></TreeView>
    <Sash location="right" :width="slider_width" @attribute_change="slider_change" />
  </l-navigation-drawer>

  <r-navigation-drawer :style="operate_style">
    <Opreate />
    <Sash location="left" :width="operate_width"  @attribute_change="operate_change" />
  </r-navigation-drawer>
  
  <main :style="main_style">
    <MainPage :content="content" :selections="selections"></MainPage>
  </main>
</template>

<script lang="ts" setup>
import Sash from '../components/Sash.vue';
import MainPage from '../layouts/MainPage.vue';
import Menu from '../layouts/Menu.vue'
import TreeView from '../layouts/TreeView.vue';
import Opreate from '../layouts/Opreate.vue';
import { ref,watch,reactive } from 'vue';
import { global_config,set_global_config,func_with_pywebview } from '~/func'

// 初始宽度
var slider_width = ref(320)
var operate_width = ref(320)

func_with_pywebview(() => {
  // 读取配置
  global_config('slider_width',(res:number)=>{
    slider_width.value = res
  })

  global_config('operate_width',(res:number)=>{
    operate_width.value = res
  });
})

var main_style = reactive({
  left: slider_width.value + 'px',
  right: operate_width.value + 'px',
})

var slider_style = reactive({
  width: slider_width.value + 'px'
})

var operate_style = reactive({
  width: operate_width.value + 'px',
})

// 监视变化，更新相关属性。

watch(slider_width, () => {
  var p = slider_width.value + 'px';
  main_style.left = p
  slider_style.width = p
  set_global_config('slider_width',slider_width.value)
});

watch(operate_width, () => {
  var p = operate_width.value + 'px';
  main_style.right = p
  operate_style.width = p
  set_global_config('operate_width',operate_width.value)
});


const slider_change = (width: number) => {
  slider_width.value = width
}
const operate_change = (width: number) => {
  operate_width.value = width
}

// 收取文件夹选择回调，并获取文件夹下的所有文件信息
var file_data = ref([])
const project_change = (data:any) => {
  file_data.value = data
}

var content = ref('')
var info = ref('None')
var selections = ref([[]])
const content_change = (text:string,infomation:string,selection:any) => {
  content.value = text
  info.value = infomation
  selections.value = selection
}
</script>

<style>
r-app-menu {
  position: absolute;
  top: 0px;
  left: 320px;
  height: 40px;
}

main {
  position: absolute;
  top: 40px;
  bottom: 0px;
}

l-navigation-drawer {
  position: absolute;
  top: 40px;
  bottom: 0px;
  left: 0px;
  background-color: aquamarine;
}

r-navigation-drawer {
  position: absolute;
  top: 40px;
  bottom: 0px;
  right: 0px;
  background-color:antiquewhite;
}
</style>