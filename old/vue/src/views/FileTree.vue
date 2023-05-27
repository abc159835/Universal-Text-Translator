<template>
    <v-card @click="test">
    <v-list density="compact" variant="elevated" min-width="200px">
        <TreeNode :date="data"  :padding="false" />
    </v-list>
</v-card>
</template>

<script setup lang="ts">
import TreeNode from '@/components/TreeNode.vue'
import { ref } from 'vue';

declare const pywebview: any;

const data = ref([]);

const test = async () => {
    data.value = await pywebview.api.get_folder_all_file('C:\\Users\\abc15\\Desktop\\Universal Translation')
    console.log(data.value)
}


</script>

<style>
</style>