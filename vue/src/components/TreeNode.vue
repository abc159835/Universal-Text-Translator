<template >
    <template v-for="([name, type, data], i) in file_date">
        <v-list-item v-if="type == 'file'" :key="i" :class=classes>
            <div>
                <v-icon icon="mdi-file" /> {{ name }}
            </div>
        </v-list-item>
        <v-list-group v-else fluid :class=classes>
            <template v-slot:activator="{ props }">
                <v-list-item :key="i" v-bind="props">
                    <div>
                        <v-icon icon="mdi-folder" /> {{ name }}
                    </div>
                </v-list-item>
            </template>
            <TreeNode :date="data" :padding="true"/>
        </v-list-group>
    </template>
</template>

<script setup lang="ts">
import TreeNode from '@/components/TreeNode.vue'

var props = defineProps<{
    date: any
    padding: boolean
}>()

// group 缩进设置
var classes = ''
if (props.padding)
    var classes = 'ml-4'

const file_date = props.date
</script>