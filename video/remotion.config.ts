import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
// Calidad alta para el render final del vídeo de la beca
Config.setCrf(18);
