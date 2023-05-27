<template>
  <div ref="editorContainer" style="height: 100%;"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted,watch } from 'vue';
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

//文本内容
var props = defineProps<{
  content:string
}>()

const editorContainer = ref(null);

var editor: monaco.editor.IStandaloneCodeEditor

const initEditor = (element: HTMLElement | null) => {
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
  editor = monaco.editor.create(element, {
    value: props.content,
    automaticLayout: true,
  });
};

watch(props, () => {
  editor.setValue(props.content)
});


onMounted(() => {
  initEditor(editorContainer.value);
});

</script>