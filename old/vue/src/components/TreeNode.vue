<template >
    <template v-for="(info, i) in file_date">
        <v-list-item v-if="info.type == 'file'" :key="i" :class=classes>
            <div>
                <v-icon icon="mdi-file" /> {{ info.name }}
            </div>
        </v-list-item>
        <v-list-group v-else fluid :class=classes>
            <template v-slot:activator="{ props }">
                <v-list-item :key="i" v-bind="props">
                    <div>
                        <v-icon icon="mdi-folder" /> {{ info.name }}
                    </div>
                </v-list-item>
            </template>
            <TreeNode :date="info.data" :padding="true"/>
        </v-list-group>
    </template>
</template>

<script setup lang="ts">
import TreeNode from '@/components/TreeNode.vue'
import { ref } from 'vue';

var props = defineProps<{
    date: any[]
    padding: boolean
}>()


// group 缩进设置
const classes = props.padding ? 'ml-4' : '';

const file_date = ref(props.date);

</script>