import * as monaco from 'monaco-editor';
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker'
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker'
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker'
import { count } from 'console';

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


export const initEditor = (element: HTMLElement) => {
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
    })
    monaco.editor.setTheme("myTheme");
    const editor = monaco.editor.create(element, {
        automaticLayout: true,
        readOnly: true
    })
    return editor
}
export const to_selections = (arrays: Array<Array<number>>) => {
    const selections = []
    for (let array of arrays)
        selections.push(new monaco.Selection(array[0], array[1], array[2], array[3]))
    return selections
}

export const decorate_selections = (selections: Array<monaco.Selection>,bools: boolean[]) => {
    const collections = []
    var count = 0
    for (let selection of selections) {
        if (bools[count])
            var collection = {
                range: selection,
                options: {
                    isWholeLine: false,
                    inlineClassName: '_InlineDecoration'
                }
            }
        else
            var collection = {
                range: selection,
                options: {
                    isWholeLine: false,
                    inlineClassName: 'InlineDecoration'
                }
            }
        collections.push(collection)
        count++
    }
    return collections
}