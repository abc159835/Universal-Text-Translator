<template>
  <v-app ref="app">
    <v-system-bar color="grey-darken-3">
      <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn max-height="20px"
          color="primary"
          dark
          v-bind="props"
        >
          Dropdown
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(item, index) in [{title:'99'}]"
          :key="index"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    </v-system-bar>

    <v-app-bar color="grey" flat height="40" location="top">
      v-app-bar,工具栏
    </v-app-bar>

    <v-navigation-drawer color="grey-darken-2" :width=slider_width permanent location="left" absolute class="custom-drawer">
      <FileTree/>
      <Sash location="right" :width="slider_width" @attribute_change="slider_change" />
    </v-navigation-drawer>

    <v-navigation-drawer color="grey-lighten-2" permanent :width=operate_width location="right">
      <Sash location="left" :width="operate_width"  @attribute_change="operate_change" />
    </v-navigation-drawer>

    <v-navigation-drawer color="grey-darken-1" permanent location="bottom" :width=search_width>
      <Sash location="top" :width=search_width @attribute_change="search_change" />
      Top,搜索视图
    </v-navigation-drawer>
    <MainPage :style="main_style_padding" class="container" />
  </v-app>
</template>

<script lang="ts" setup>
import MainPage from '@/views/MainPage.vue';
import FileTree from '@/views/FileTree.vue'
import Sash from '@/components/Sash.vue';
import { ref } from 'vue';

var slider_width = ref(200)
var operate_width = ref(160)
var search_width = ref(60)
var app = ref(null)

var main_style_padding = {
  left: slider_width.value + 'px',
  right: operate_width.value + 'px',
  bottom: search_width.value + 'px',
}

const change = () => {
  main_style_padding = {
    left: slider_width.value + 'px',
    right: operate_width.value + 'px',
    bottom: search_width.value + 'px',
  }
}

const slider_change = (width: number) => {
  slider_width.value = width
  change()
}
const operate_change = (width: number) => {
  operate_width.value = width
  change()
}
const search_change = (width: number) => {
  search_width.value = width
  change()
}

</script>

<style>
/* 隐藏滚动条样式 */
body::-webkit-scrollbar {
  width: 0;
  height: 0;
  background-color: transparent;
}


.container {
  position: absolute;
  top: 64px;
}

.custom-drawer ::-webkit-scrollbar {
  width: 8px; /* 滚动条宽度 */
  background-color: #f5f5f5; /* 滚动条背景色 */
}

.custom-drawer ::-webkit-scrollbar-thumb {
  background-color: #888; /* 滚动条滑块颜色 */
}

.custom-drawer ::-webkit-scrollbar-thumb:hover {
  background-color: #555; /* 滚动条滑块悬停时颜色 */
}
</style>