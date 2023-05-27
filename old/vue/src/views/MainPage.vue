<template>
  <div ref="editorContainer"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as monaco from 'monaco-editor';
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker'
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker'
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker'

self.MonacoEnvironment = {
  getWorker(_, label) {
    if (label === 'json') {
      return new jsonWorker()
    }
    if (label === 'css' || label === 'scss' || label === 'less') {
      return new cssWorker()
    }
    if (label === 'html' || label === 'handlebars' || label === 'razor') {
      return new htmlWorker()
    }
    if (label === 'typescript' || label === 'javascript') {
      return new tsWorker()
    }
    return new editorWorker()
  }
}

const editorContainer = ref(null);


const initEditor = function (element: HTMLElement | null) {
  if (!element) return;
  monaco.editor.defineTheme("myTheme", {
    base: "vs",
    inherit: true,
    rules: [],
    colors: {
      "editor.foreground": "#000000",
      "editor.background": "#EDF9FA",
      "editorCursor.foreground": "#8B0000",
      "editor.lineHighlightBackground": "#0000FF20",
      "editorLineNumber.foreground": "#008800",
      "editor.selectionBackground": "#88000030",
      "editor.inactiveSelectionBackground": "#88000015",
    },
  });
  monaco.editor.setTheme("myTheme");
  monaco.editor.create(element, {
    value: '',
    automaticLayout: true,
  });
};

onMounted(() => {
  initEditor(editorContainer.value);
});
</script>

<style>

</style>
