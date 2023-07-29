<template>
  <el-scrollbar height="100%">
    <el-card style="border-radius: 0px">
      <el-space wrap style="display: flex; justify-content: center;">
        <el-switch
          v-model="no_raw"
          class="mb-2"
          active-text="Translation"
          size="large"
          inline-prompt
          style="--el-switch-on-color: rgb(1, 202, 78); --el-switch-off-color: grey;"
          @click="emit('handle_click','change')"
          inactive-text="Raw"
        />
        
      </el-space>
      <el-input :model-value="original_text" :rows="5" type="textarea" placeholder="Original text displayed here" />
      <el-divider />
      <el-space wrap style="display: flex; justify-content: center;">
        <el-button type="primary" @click="emit('handle_click','back')">Back</el-button>
        <el-button type="primary" @click="emit('handle_click','next')">Next</el-button>
        <el-button type="primary" @click="emit('handle_click','submit')">Submit</el-button>
        <el-button :loading="loading" type="success" @click="emit('handle_click','translate')">Translate</el-button>
      </el-space>
      <el-slider v-model="posi" :max="line_count" :min="line_count > 0 ? 1 : 0" @input="emit('handle_click',posi)" :step="1"/>
      <el-divider />
      <el-input :model-value="modelValue" @input="res => emit('update:modelValue',res)" :rows="5" type="textarea" placeholder="Translation displayed here" />
    </el-card>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { watch,ref } from 'vue'


const p = defineProps<{
  original_text: string
  line_count: number
  modelValue: string
  position: number
  loading: boolean
  raw: boolean
}>()

const emit = defineEmits(['handle_click','update:modelValue'])
var posi = p.position
var no_raw = ref(!p.raw)

watch(p,() => {
  posi = p.position
  no_raw.value = !p.raw
})


</script>

<style></style>