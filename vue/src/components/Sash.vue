<template>
    <div :style=style :class=_class @mousedown="mousedown" v-show=on_show></div>
</template>

<script lang="ts" setup>
import { throttle } from '~/func'




// props透传
var props = defineProps<{
    location: string
    width: number
}>()

// 事件声明
var emit = defineEmits<{
    (event: 'attribute_change', value: number): void
}>()

var style = {
    cursor: "auto",
    width: "",
    height: "",
}
var X = true
var _class = props.location

if (props.location == 'top' || props.location == 'bottom') {
    style.cursor = 'row-resize'
    style.width = "100%"
    style.height = "8px"
    X = false
}
else if (props.location == 'left' || props.location == 'right') {
    style.cursor = 'col-resize'
    style.width = "8px"
    style.height = "100%"
}

var on_show = true
// 父控件的width
var width = 0
// cursor的初始位置
var start = 0

// 发送新的width
const send = (event: MouseEvent) => {
    var shifting = 0
    var res = 0
    var edge = 6
    if (X)
        shifting = event.clientX - start
    else
        shifting = event.clientY - start
    if (props.location == 'left' || props.location == 'top')
        res = width - shifting
    else
        res = width + shifting

    // 使之还能被拖出
    if (res < edge)
        res = edge
    emit('attribute_change', res)
}

const th_send = throttle(send, 10)

const mousemove = (event: MouseEvent) => {
    th_send(event)
}
const mousedown = (event: MouseEvent) => {
    // 浏览器不执行事件的默认行为
    event.preventDefault();
    // 确定初始位置
    if (X)
        start = event.clientX
    else
        start = event.clientY

    // 记录改变开始时的width
    width = props.width
    window.addEventListener('mousemove', mousemove);
    window.addEventListener('mouseup', mouseup);
}
const mouseup = (event: MouseEvent) => {
    send(event)
    window.removeEventListener('mousemove', mousemove);
    window.removeEventListener('mouseup', mouseup);
}

</script>

<style>
.bottom {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
}

.left {
  position: absolute;
  left: 0;
  bottom: 0;
  top: 0;
}

.right {
  position: absolute;
  right: 0;
  bottom: 0;
  top: 0;
}

.top {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}
</style>