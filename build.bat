cd vue
yarn build && pause && cd .. && xcopy "vue\dist" "dist\Application\static" /E /I /H /Y && pause