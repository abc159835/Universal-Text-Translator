cd vue
yarn build && pause && cd .. && xcopy "vue\dist" "dist\Application\static" /E /I /H /Y && xcopy "vue\dist" "UTT\Application\static" /E /I /H /Y && pause