<template>
  <el-scrollbar height="100%">
    <el-card style="border-radius: 0px">
      <el-space wrap style="display: flex; justify-content: center;">
        <el-button type="success">Pre Translation</el-button>
      </el-space>
      <el-divider />
      <el-input v-model="textarea1" type="textarea" placeholder="Original text displayed here" />
      <el-divider />
      <el-space wrap style="display: flex; justify-content: center;">
        <el-button type="primary">Back</el-button>
        <el-button type="primary">Next</el-button>
        <el-button type="success">Translate</el-button>
      </el-space>
      <el-divider />
      <el-input v-model="textarea2" type="textarea" placeholder="Translation displayed here" />
    </el-card>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
const textarea1 = ref('')
const textarea2 = ref('')
</script>

<style></style>