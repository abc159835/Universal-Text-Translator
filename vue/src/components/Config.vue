<template>
    <el-form :label-width="labelWidth+'px'" label-position="right" v-for="value, key in config">
        <el-form-item v-if="(typeof value == 'number')" :label="key">
            <el-input-number v-model="config[key]"/>
        </el-form-item>
        <el-form-item v-else-if="(Array.isArray(value) && typeof value[0] == 'string')" :label="key">
            <el-select v-model="config[key][0]" placeholder="Select">
                <el-option v-for="item in value[1]" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>
        <el-form-item v-else-if="(Array.isArray(value) && typeof value[0] == 'number')" :label="key">
            <el-slider v-model="config[key][0]" :max="value[1]['max']" :min="value[1]['min']" :step="value[1]['step']" />
        </el-form-item>
        <el-form-item v-else-if="(typeof value == 'string')" :label="key">
            <el-input v-model="config[key]" type="textarea" autosize/>
        </el-form-item>
    </el-form>
</template>

<script setup lang="ts">
import { ElSelect, ElSlider } from 'element-plus';

// props透传
var props = defineProps<{
    config: {}
    labelWidth: number
}>()
</script>